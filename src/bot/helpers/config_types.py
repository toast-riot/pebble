from typing import Generic, TypeVar, get_type_hints, get_origin, get_args
from types import UnionType, NoneType

UNSET = object()
KT = TypeVar('KT')
VT = TypeVar('VT')


class ConfigObj():
    @property
    def _data(self):
        return self._to_dict(self.__dict__)

    @classmethod
    def _to_dict(self, obj):
        if isinstance(obj, (str, int, float, bool, NoneType)):
            return obj
        elif isinstance(obj, dict):
            return {k: self._to_dict(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._to_dict(item) for item in obj]
        elif isinstance(obj, ConfigObj):
            return self._to_dict(obj._data)
        else:
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    def _hint(self, attr_name: str):
        type_hints = get_type_hints(self)
        if attr_name in type_hints: return type_hints[attr_name]
        raise AttributeError(f"Attribute '{attr_name}' not found in type hints for {self.__name__}")


class AutoDict(dict, Generic[KT, VT]):
    def __init__(self, default_factory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default_factory = default_factory

    def __getitem__(self, key: KT) -> VT:
        if key not in self:
            self[key] = self._default_factory()
        return super().__getitem__(key)


def json_type_validate(value, expected) -> bool:
    """
    Basic type validation for JSON-like structures.
    """
    def is_supported_type(t):
        return t in (NoneType, bool, str, int, float, list, dict)

    if is_supported_type(expected): return type(value) is expected

    if is_supported_type(type(expected)):
        return (type(value) is type(expected)) and (value == expected)

    origin = get_origin(expected)

    if origin is UnionType:
        args = get_args(expected)
        for arg in args: json_type_validate(None, arg)
        return any(json_type_validate(value, arg) for arg in args)

    if origin is list:
        args = get_args(expected)
        if len(args) != 1: raise TypeError(f"Expected a single type argument for list, got {args}")
        is_instance = type(value) is origin
        if not is_instance or len(value) == 0: json_type_validate(None, args[0])
        return is_instance and all(json_type_validate(item, args[0]) for item in value)

    if origin is dict:
        args = get_args(expected)
        if len(args) != 2: raise TypeError(f"Expected two type arguments for dict, got {args}")
        is_instance = type(value) is origin
        if not is_instance or len(value) == 0: [json_type_validate(None, arg) for arg in args]
        return is_instance and all(json_type_validate(k, args[0]) and json_type_validate(v, args[1]) for k, v in value.items())

    raise ValueError(f"Unsupported type: {expected}")


def cfg(config: dict, value: str, expected_type = UNSET, default = UNSET):
    if value not in config:
        if default is UNSET:
            raise KeyError(f"Key '{value}' not found")
        value = default
    else:
        value = config[value]
    if (expected_type is not UNSET) and not json_type_validate(value, expected_type):
        raise TypeError(f"Value {value} does not match expected type {expected_type}")
    return value


def create_auto_dict(key_type: type, val_type: ConfigObj, vals: dict) -> 'AutoDict[KT, VT]':
    return AutoDict(lambda: val_type(), {key_type(k): val_type(v) for k, v in vals.items()})