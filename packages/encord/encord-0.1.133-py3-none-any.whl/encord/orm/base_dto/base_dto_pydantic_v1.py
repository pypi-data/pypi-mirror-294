import json
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Dict, Literal, Type, TypeVar

from pydantic import BaseModel, Field, PrivateAttr, ValidationError, root_validator, validator
from pydantic.generics import GenericModel

from encord.common.time_parser import parse_datetime
from encord.common.utils import snake_to_camel
from encord.exceptions import EncordException
from encord.orm.base_dto.base_dto_interface import BaseDTOInterface, T


class BaseDTO(BaseDTOInterface, BaseModel):
    class Config:
        ignore_extra = True
        alias_generator = snake_to_camel
        allow_population_by_field_name = True

    @validator("*", pre=True)
    def parse_datetime(cls, value, field):
        if isinstance(value, str) and issubclass(field.type_, datetime):
            return parse_datetime(value)
        return value

    @classmethod
    def from_dict(cls: Type[T], d: Dict[str, Any]) -> T:
        try:
            return cls.parse_obj(d)  # type: ignore[attr-defined]
        except ValidationError as e:
            raise EncordException(message=str(e)) from e

    def to_dict(self, by_alias=True, exclude_none=True) -> Dict[str, Any]:
        # Pydantic v1 is missing the 'model_dump()' method, the below is suboptimal but works
        return json.loads(self.json(by_alias=by_alias, exclude_none=exclude_none))  # type: ignore[attr-defined]


DataT = TypeVar("DataT")


class GenericBaseDTO(BaseDTOInterface, GenericModel):
    class Config:
        ignore_extra = True
        alias_generator = snake_to_camel
        allow_population_by_field_name = True

    @validator("*", pre=True)
    def parse_datetime(cls, value, field):
        if isinstance(value, str) and issubclass(field.type_, datetime):
            return parse_datetime(value)
        return value

    @classmethod
    def from_dict(cls: Type[T], d: Dict[str, Any]) -> T:
        try:
            return cls.parse_obj(d)  # type: ignore[attr-defined]
        except ValidationError as e:
            raise EncordException(message=str(e)) from e

    def to_dict(self, by_alias=True, exclude_none=True) -> Dict[str, Any]:
        # Pydantic v1 is missing the 'model_dump()' method, the below is suboptimal but works
        return json.loads(self.json(by_alias=by_alias, exclude_none=exclude_none))  # type: ignore[attr-defined]


def dto_validator(mode: Literal["before", "after"] = "before") -> Callable:
    def decorator(func: Callable) -> Callable:
        return root_validator(pre=(mode == "before"))(func)  # type: ignore

    return decorator
