from typing import Any, Type, Union


class DimoError(Exception):
    """Base class for execeptions"""

    pass


class DimoTypeError(DimoError):
    def __init__(
        self, param_name: str, expected_type: Union[Type, tuple], actual_value: Any
    ):
        self.param_name = param_name
        self.expected_type = expected_type
        self.actual_value = actual_value
        self.message = f"{param_name} must be a {expected_type.__name__}, but was entered as type {type(actual_value).__name__}."
        super().__init__(self.message)


def check_type(param_name: str, value: Any, expected_type: Union[Type, tuple]):
    if not isinstance(value, expected_type):
        raise DimoTypeError(param_name, expected_type, value)


def check_optional_type(param_name: str, value: Any, expected_type: Union[Type, tuple]):
    if value is not None and not isinstance(value, expected_type):
        raise DimoTypeError(param_name, expected_type, value)


class DimoValueError(DimoError):
    pass
