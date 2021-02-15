from .device import AbstractDevice


class jkbms(AbstractDevice):
    def __init__(self, *args, **kwargs) -> None:
        self._classname = "jkbms"
        super().__init__(*args, **kwargs)
