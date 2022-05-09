import datetime
import logging
import re
import time

import psycopg2 as psycopg2
from psycopg2._json import Json

from . import to_json, get_common_params
from .baseoutput import baseoutput
from ..helpers import get_kwargs
from ..helpers import key_wanted
from psycopg2.extensions import register_adapter

log = logging.getLogger("postgres")


class postgres(baseoutput):
    def __str__(self):
        return "outputs all the results to PostgresSQL"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"__init__: kwargs {kwargs}")
        register_adapter(dict, Json)

    # run in advance: sudo apt-get install libpq-dev
    # create table mppsolar
    # (
    #     id      serial
    #         constraint mppsolar_pk
    #             primary key,
    #     data    json,
    #     command varchar
    # );

    def output(self, *args, **kwargs):
        (data, tag, keep_case, filter_, excl_filter) = get_common_params(kwargs)

        postgres_url = get_kwargs(kwargs, "postgres_url")
        log.debug(f"Connecting to {postgres_url}")
        conn = psycopg2.connect(postgres_url)

        msgs = []
        # Remove command and _command_description
        # cmd = data.pop("_command", None)
        data.pop("_command_description", None)
        data.pop("raw_response", None)
        # if tag is None:
        #     tag = cmd
        output = to_json(data, keep_case, excl_filter, filter_)

        log.debug(output)
        msgs.append(output)
        inserted = 0
        try:
            for msg in msgs:
                command = msg.pop("_command")
                msg['updated'] = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.gmtime())
                log.debug(conn)
                cursor = conn.cursor()
                log.debug(cursor)
                cursor.execute("insert into mppsolar (command,data) values (%s,%s)", (command, msg))
                conn.commit()
                inserted += 1
                cursor.close()
            log.debug(f"inserted {inserted} docs")
        except Exception as e:
            log.error(f"Postgres error {e}")
        finally:
            conn.close()
        return msgs
