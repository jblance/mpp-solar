""" errors.py - collection of powermon specific exceptions """


class ConfigError(Exception):
    """Exception for invaild configurations"""


class PowermonProtocolError(Exception):
    """Exception for errors with protocol definitions"""


class PowermonWIP(Exception):
    """Exception for work not yet done"""
