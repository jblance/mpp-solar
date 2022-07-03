import logging
from datetime import datetime

import psycopg2 as psycopg2
from psycopg2._json import Json
from psycopg2.extensions import register_adapter

from . import to_json, get_common_params
from .baseoutput import baseoutput
from ..helpers import get_kwargs

log = logging.getLogger("postgres")

"""
To use, run `sudo apt-get install libpq-dev`

Creating table in Postgresql in advance:

-- auto-generated definition
create table mppsolar
(
    id      serial
        constraint mppsolar_pk
            primary key,
    command varchar,
    data    json,
    updated timestamp
);

create index mppsolar_command_updated_index
    on mppsolar (command, updated);


"""


class postgres(baseoutput):
    def __str__(self):
        return "outputs all the results to PostgresSQL"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"__init__: kwargs {kwargs}")
        register_adapter(dict, Json)

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
        now = datetime.now().astimezone().replace(microsecond=0).isoformat()
        try:
            for msg in msgs:
                command = msg.pop("_command")
                msg['updated'] = now
                log.debug(conn)
                cursor = conn.cursor()
                log.debug(cursor)
                cursor.execute('insert into mppsolar (command,data, updated) values (%s,%s,%s)', (command, msg, now))
                conn.commit()
                inserted += 1
                cursor.close()
            log.debug(f"inserted {inserted} docs")
        except Exception as e:
            log.error(f"Postgres error {e}")
        finally:
            conn.close()
        return msgs
