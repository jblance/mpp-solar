from .device import AbstractDevice


class mppsolar(AbstractDevice):
    def __init__(self, *args, **kwargs) -> None:
        self._classname = "mppsolar"
        super().__init__(*args, **kwargs)
