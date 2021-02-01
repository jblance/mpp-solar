import logging


log = logging.getLogger("MPP-Solar")


class baseoutput:
    def __str__(self):
        return "the base class for the output processors, not used directly"

    def get_kwargs(self, kwargs, key, default=None):
        if not key in kwargs or not kwargs[key]:
            return default
        return kwargs[key]
