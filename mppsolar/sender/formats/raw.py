from mppsolar.helpers import get_kwargs


class raw:
    def output(*args, **kwargs):
        # print(args, kwargs)
        _data = get_kwargs(kwargs, "data", None)
        if "raw_response" in _data:
            _result = _data["raw_response"][0]
            return _result
