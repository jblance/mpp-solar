import socket
import sys
import threading
import time

import pytest

from mppsolar.inout.hidrawio import HIDRawIO

pytestmark = pytest.mark.skipif(sys.platform != "linux", reason="Linux hidraw transport")


@pytest.fixture
def reports():
    # Preserve HID report boundaries while using real nonblocking file I/O.
    if not hasattr(socket, "SOCK_SEQPACKET"):
        pytest.skip("requires Unix sequenced-packet sockets")
    reader, writer = socket.socketpair(socket.AF_UNIX, socket.SOCK_SEQPACKET)
    reader.setblocking(False)
    try:
        yield reader, writer
    finally:
        reader.close()
        writer.close()


def test_buffered_hid_reports_do_not_consume_timeout(reports):
    reader, writer = reports
    response = b"(" + b"1234567890 " * 10 + b"\r"
    for start in range(0, len(response), 8):
        writer.send(response[start:start + 8].ljust(8, b"\0"))
    port = HIDRawIO("unused", timeout=0.6)
    assert port._receive_response(reader.fileno()) == response


def test_waits_for_delayed_reports(reports):
    reader, writer = reports

    def deliver():
        time.sleep(0.03)
        writer.send(b"(1234567")
        time.sleep(0.03)
        writer.send(b"89\r\0\0\0\0\0")

    producer = threading.Thread(target=deliver)
    producer.start()
    try:
        assert HIDRawIO("unused", timeout=1)._receive_response(reader.fileno()) == b"(123456789\r"
    finally:
        producer.join()


@pytest.mark.parametrize("partial", [b"", b"(unfinished"])
def test_incomplete_response_times_out(reports, partial):
    reader, writer = reports
    if partial:
        writer.send(partial)
    with pytest.raises(TimeoutError):
        HIDRawIO("unused", timeout=0.1)._receive_response(reader.fileno())


def test_readiness_race_retries_within_deadline(reports, monkeypatch):
    import errno
    import os

    reader, writer = reports
    writer.send(b"(ready\r")
    original_read = os.read
    raced = False

    def read(fd, count):
        nonlocal raced
        if fd == reader.fileno() and not raced:
            raced = True
            raise BlockingIOError(errno.EAGAIN, "report no longer ready")
        return original_read(fd, count)

    monkeypatch.setattr(os, "read", read)
    assert HIDRawIO("unused", timeout=1)._receive_response(reader.fileno()) == b"(ready\r"
    assert raced


def test_disconnected_device_reports_io_error(reports):
    import errno

    reader, writer = reports
    writer.close()
    with pytest.raises(OSError) as error:
        HIDRawIO("unused", timeout=1)._receive_response(reader.fileno())
    assert error.value.errno == errno.EIO
