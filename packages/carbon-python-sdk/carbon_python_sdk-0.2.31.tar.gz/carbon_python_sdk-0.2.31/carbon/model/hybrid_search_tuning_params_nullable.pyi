# coding: utf-8

"""
    Carbon

    Connect external data to LLMs, no matter the source.

    The version of the OpenAPI document: 1.0.0
    Generated by: https://konfigthis.com
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from carbon import schemas  # noqa: F401


class HybridSearchTuningParamsNullable(
    schemas.DictBase,
    schemas.NoneBase,
    schemas.Schema,
    schemas.NoneFrozenDictMixin
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    Hybrid search tuning parameters. See the endpoint description for more details.
    """


    class MetaOapg:
        required = {
            "weight_a",
            "weight_b",
        }
        
        class properties:
            weight_a = schemas.NumberSchema
            weight_b = schemas.NumberSchema
            __annotations__ = {
                "weight_a": weight_a,
                "weight_b": weight_b,
            }

    
    weight_a: MetaOapg.properties.weight_a
    weight_b: MetaOapg.properties.weight_b
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["weight_a"]) -> MetaOapg.properties.weight_a: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["weight_b"]) -> MetaOapg.properties.weight_b: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["weight_a", "weight_b", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["weight_a"]) -> MetaOapg.properties.weight_a: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["weight_b"]) -> MetaOapg.properties.weight_b: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["weight_a", "weight_b", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, None, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'HybridSearchTuningParamsNullable':
        return super().__new__(
            cls,
            *args,
            _configuration=_configuration,
            **kwargs,
        )
