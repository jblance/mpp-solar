#!/usr/bin/env python3
import logging
import re

log = logging.getLogger("helpers")


def get_kwargs(kwargs, key, default=None):
    if not key in kwargs or not kwargs[key]:
        return default
    return kwargs[key]


def key_wanted(key, filter=None, excl_filter=None):
    # remove any specifically excluded keys
    if excl_filter is not None and excl_filter.search(key):
        log.debug(f"key_wanted: key {key} matches excl_filter {excl_filter} so key excluded")
        return False
    if filter is None:
        log.debug(
            f"key_wanted: No filter and key {key} not excluded by excl_filter {excl_filter} so key wanted"
        )
        return True
    elif filter.search(key):
        log.debug(
            f"key_wanted: key {key} matches filter {filter} and not excl_filter {excl_filter} so key wanted"
        )
        return True
    else:
        log.debug(f"key_wanted: key {key} does not match filter {filter} so key excluded")
        return False


def get_resp_defn(key, defns):
    """
    look for a definition for the supplied key
    """
    # print(key, defns)
    if not key:
        return None
    try:
        key = key.decode("utf-8")
    except UnicodeDecodeError as e:
        log.info(f"get_resp_defn: key decode error for {key}")
    for defn in defns:
        if key == defn[0]:
            # print(key, defn)
            return defn
    # did not find definition for this key
    log.info(f"No defn found for {key} key")
    return [key, key, "", ""]
