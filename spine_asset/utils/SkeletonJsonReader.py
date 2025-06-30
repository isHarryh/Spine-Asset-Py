from enum import Enum
from typing import Any, Collection, Dict, List, Optional, Tuple, Union, TypeVar, Type

import json
import re

_E = TypeVar("_E", bound=Enum)
_DEFAULT_STRING_TYPE = TypeVar("_DEFAULT_STRING_TYPE")


class SkeletonJsonReader:
    """Reader for basic data types in Spine JSON format skeleton."""

    def __init__(self, data: Union[str, bytes, Dict[str, Any]]):
        if isinstance(data, dict):
            self._json = data
        elif isinstance(data, (str, bytes)):
            self._json = json.loads(data)
        else:
            raise ValueError("Data must be string, bytes, or dict")

    def get_raw(self, key: str, default: Any = None) -> Any:
        return self._json.get(key, default)

    def get_bool(self, key: str, default: bool = False) -> bool:
        value = self._json.get(key, default)
        if not isinstance(value, bool):
            raise TypeError(f"Expected bool for key '{key}', got {type(value).__name__}")
        return value

    def get_int(self, key: str, default: int = 0) -> int:
        value = self._json.get(key, default)
        if not isinstance(value, (int, float)):
            raise TypeError(f"Expected number for key '{key}', got {type(value).__name__}")
        return int(value)

    def get_float(self, key: str, default: float = 0.0) -> float:
        value = self._json.get(key, default)
        if not isinstance(value, (int, float)):
            raise TypeError(f"Expected number for key '{key}', got {type(value).__name__}")
        return float(value)

    def get_string(self, key: str, default: _DEFAULT_STRING_TYPE) -> Union[str, _DEFAULT_STRING_TYPE]:
        value = self._json.get(key, default)
        if value is None:
            return default
        if isinstance(value, str):
            return value
        raise TypeError(f"Expected str for key '{key}', got {type(value).__name__}")

    def get_string_required(self, key: str) -> str:
        if key not in self._json:
            raise ValueError(f"Required key '{key}' not found")

        value = self._json.get(key)
        if not isinstance(value, str):
            raise TypeError(f"Expected str for key '{key}', got {type(value).__name__}")
        return value

    def get_child(self, key: str) -> "SkeletonJsonReader":
        if key not in self._json:
            raise ValueError(f"Required key '{key}' not found")

        value = self._json.get(key)
        if not isinstance(value, dict):
            raise TypeError(f"Expected dict for key '{key}', got {type(value).__name__}")
        return SkeletonJsonReader(value)

    def get_list(self, key: str, required: bool = False) -> List[Any]:
        if key not in self._json:
            if required:
                raise ValueError(f"Required key '{key}' not found")
            else:
                return []

        value = self._json.get(key)
        if not isinstance(value, list):
            raise TypeError(f"Expected list for key '{key}', got {type(value).__name__}")
        return value

    def get_color(self, key: str, required: bool = False) -> Optional[Tuple[float, float, float, float]]:
        color_str = self._json.get(key, None)
        if not color_str:
            if required:
                raise ValueError(f"Required key '{key}' not found")
            else:
                return None

        if not isinstance(color_str, str):
            raise TypeError(f"Expected str for color key '{key}', got {type(color_str).__name__}")

        if len(color_str) == 8:
            return (
                int(color_str[0:2], 16) / 255.0,
                int(color_str[2:4], 16) / 255.0,
                int(color_str[4:6], 16) / 255.0,
                int(color_str[6:8], 16) / 255.0,
            )
        elif len(color_str) == 6:
            return (
                int(color_str[0:2], 16) / 255.0,
                int(color_str[2:4], 16) / 255.0,
                int(color_str[4:6], 16) / 255.0,
                1.0,
            )
        raise ValueError(f"Invalid color format for key '{key}': {color_str}. Expected 6 or 8 hex digits.")

    def get_enum(self, key: str, enum_class: Type[_E], default: _E) -> _E:
        value = self._json.get(key)
        if not value:
            return default

        if not isinstance(value, str):
            raise TypeError(f"Expected str for enum key '{key}', got {type(value).__name__}")

        snake_case_value = re.sub("([a-z0-9])([A-Z])", r"\1_\2", value).upper()
        try:
            return getattr(enum_class, snake_case_value)
        except AttributeError:
            try:
                return getattr(enum_class, value.upper())
            except AttributeError:
                return default

    def iter_child_keys(self, key: str, required: bool = False):
        if key in self._json:
            value = self._json[key]
            if not isinstance(value, dict):
                raise TypeError(f"Expected dict for key '{key}' to iterate, got {type(value).__name__}")
            yield from value.keys()
        elif required:
            raise KeyError(key)

    def iter_child_dict(self, key: str, required: bool = False):
        if key in self._json:
            value = self._json[key]
            if not isinstance(value, dict):
                raise TypeError(f"Expected dict for key '{key}' to iterate, got {type(value).__name__}")
            for sub_key, sub_value in value.items():
                if not isinstance(sub_key, str):
                    raise TypeError(f"Expected str sub key to iterate, got {type(sub_key).__name__}")
                yield sub_key, SkeletonJsonReader(sub_value)
        elif required:
            raise KeyError(key)

    def iter_child_list(self, key: str, required: bool = False):
        if key in self._json:
            value = self._json[key]
            if not isinstance(value, list):
                raise TypeError(f"Expected list for key '{key}' to iterate, got {type(value).__name__}")
            for sub_value in value:
                yield SkeletonJsonReader(sub_value)
        elif required:
            raise KeyError(key)

    def keys(self) -> Collection[str]:
        return self._json.keys()

    def __contains__(self, key: str) -> bool:
        return key in self._json

    def __len__(self) -> int:
        return len(self._json)
