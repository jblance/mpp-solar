import datetime
import logging
import re

import pymongo as pymongo

from . import to_json
from .baseoutput import baseoutput
from ..helpers import get_kwargs
from ..helpers import key_wanted

log = logging.getLogger("mongo")


class mongo(baseoutput):
    def __str__(self):
        return "outputs all the results to MongoDB"

    def __init__(self, *args, **kwargs) -> None:
        log.debug(f"__init__: kwargs {kwargs}")

    def output(self, *args, **kwargs):
        data = get_kwargs(kwargs, "data")
        tag = get_kwargs(kwargs, "tag")
        keep_case = get_kwargs(kwargs, "keep_case")
        filter = get_kwargs(kwargs, "filter")
        if filter is not None:
            filter = re.compile(filter)
        excl_filter = get_kwargs(kwargs, "excl_filter")
        if excl_filter is not None:
            excl_filter = re.compile(excl_filter)

        mongo_url = get_kwargs(kwargs, "mongo_url")
        mongo_database = get_kwargs(kwargs, "mongo_db", "mppsolar")
        log.debug(f"Connecting to {mongo_url} / {mongo_database}")
        client = pymongo.MongoClient(mongo_url)
        db = client[mongo_database]

        msgs = []
        # Remove command and _command_description
        # cmd = data.pop("_command", None)
        data.pop("_command_description", None)
        data.pop("raw_response", None)
        # if tag is None:
        #     tag = cmd
        output = to_json(data, keep_case, excl_filter, filter)

        log.debug(output)
        msgs.append(output)
        inserted = 0
        try:
            for msg in msgs:
                col = msg.pop("_command")
                msg['updated'] = datetime.datetime.now()
                result = db[col].insert_one(msg)
                if result is not None:
                    log.debug(result.inserted_id)
                    inserted += 1
            log.debug(f"inserted {inserted} docs")
        except pymongo.errors.ServerSelectionTimeoutError as dbe:
            log.error(f"Mongo error {dbe}")
        return msgs
