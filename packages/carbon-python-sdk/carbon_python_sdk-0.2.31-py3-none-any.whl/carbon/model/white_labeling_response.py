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


class WhiteLabelingResponse(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        required = {
            "custom_limits",
            "remove_branding",
            "integrations",
        }
        
        class properties:
            remove_branding = schemas.BoolSchema
            integrations = schemas.DictSchema
            custom_limits = schemas.DictSchema
            __annotations__ = {
                "remove_branding": remove_branding,
                "integrations": integrations,
                "custom_limits": custom_limits,
            }
    
    custom_limits: MetaOapg.properties.custom_limits
    remove_branding: MetaOapg.properties.remove_branding
    integrations: MetaOapg.properties.integrations
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["remove_branding"]) -> MetaOapg.properties.remove_branding: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["integrations"]) -> MetaOapg.properties.integrations: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["custom_limits"]) -> MetaOapg.properties.custom_limits: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["remove_branding", "integrations", "custom_limits", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["remove_branding"]) -> MetaOapg.properties.remove_branding: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["integrations"]) -> MetaOapg.properties.integrations: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["custom_limits"]) -> MetaOapg.properties.custom_limits: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["remove_branding", "integrations", "custom_limits", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        custom_limits: typing.Union[MetaOapg.properties.custom_limits, dict, frozendict.frozendict, ],
        remove_branding: typing.Union[MetaOapg.properties.remove_branding, bool, ],
        integrations: typing.Union[MetaOapg.properties.integrations, dict, frozendict.frozendict, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'WhiteLabelingResponse':
        return super().__new__(
            cls,
            *args,
            custom_limits=custom_limits,
            remove_branding=remove_branding,
            integrations=integrations,
            _configuration=_configuration,
            **kwargs,
        )
