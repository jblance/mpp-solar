#!/usr/bin/env python3
import logging
import re

log = logging.getLogger("MPP-Solar")


def get_kwargs(kwargs, key, default=None):
    if not key in kwargs or not kwargs[key]:
        return default
    return kwargs[key]


def key_wanted(key, filter=None, excl_filter=None):
    # remove any specifically excluded keys
    if excl_filter is not None and excl_filter.search(key):
        log.debug(f"key {key} matches excl_filter {excl_filter} so key excluded")
        return False
    if filter is None:
        log.info(f"No filter and key {key} not excluded by excl_filter {excl_filter} so key wanted")
        return True
    elif filter.search(key):
        log.info(
            f"key {key} matches filter {filter} and not excl_filter {excl_filter} so key wanted"
        )
        return True
    else:
        log.debug(f"key {key} does not match filter {filter} so key excluded")
        return False
