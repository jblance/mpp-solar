#!/usr/bin/env python3
import logging

log = logging.getLogger("MPP-Solar")


def get_kwargs(kwargs, key, default=None):
    if not key in kwargs or not kwargs[key]:
        return default
    return kwargs[key]
