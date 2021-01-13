import logging


log = logging.getLogger("MPP-Solar")


class BaseOutput:
    def get_kwargs(self, kwargs, key, default=None):
        if not key in kwargs or not kwargs[key]:
            return default
        return kwargs[key]
