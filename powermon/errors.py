""" errors.py - collection of powermon specific exceptions """


class ConfigError(Exception):
    """ Exception for invaild configurations """


class PowermonProtocolError(Exception):
    """ Exception for errors with protocol definitions """


class PowermonWIP(Exception):
    """ Exception for work not yet done """


class InvalidResponse(Exception):
    """ Exception for invalid responses """


class InvalidCRC(Exception):
    """ Exception for invalid crc """


class CommandDefinitionMissing(Exception):
    """ Exception for missing / not found command definition """


class CommandError(Exception):
    """ Exception for errors with commands """
