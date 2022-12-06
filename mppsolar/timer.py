import threading
import time
from time import sleep


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


if __name__ == "__main__":
    # main()
    def hello(name):
        global lock
        print("Hello %s! lock=%s" % (name, lock))
        lock = not lock
    lock = False
    # some_lock = threading.Lock()
    # with some_lock:
    #     # do something...
    # is equivalent to:
    # some_lock.acquire()
    # try:
    #     # do something...
    # finally:
    #     some_lock.release()
    print("starting...")
    rt = RepeatedTimer(2, hello, "World")  # it auto-starts, no need of rt.start()
    rt2 = RepeatedTimer(3, hello, "Bob")
    try:
        sleep(20)  # your long-running job goes here...
    finally:
        rt.stop()  # better in a try/finally block to make sure the program ends!
        rt2.stop()
