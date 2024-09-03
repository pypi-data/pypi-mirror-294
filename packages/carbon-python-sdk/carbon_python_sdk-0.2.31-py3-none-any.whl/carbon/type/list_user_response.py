# coding: utf-8

"""
    Carbon

    Connect external data to LLMs, no matter the source.

    The version of the OpenAPI document: 1.0.0
    Generated by: https://konfigthis.com
"""

from datetime import datetime, date
import typing
from enum import Enum
from typing_extensions import TypedDict, Literal, TYPE_CHECKING

from carbon.type.list_user_response_auto_sync_enabled_sources import ListUserResponseAutoSyncEnabledSources

class RequiredListUserResponse(TypedDict):
    id: int

    organization_id: int

    organization_supplied_user_id: str

    created_at: datetime

    updated_at: datetime

    deleted_at: typing.Optional[datetime]

    enabled_features: typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]]

    custom_limits: typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]

    auto_sync_enabled_sources: ListUserResponseAutoSyncEnabledSources

class OptionalListUserResponse(TypedDict, total=False):
    pass

class ListUserResponse(RequiredListUserResponse, OptionalListUserResponse):
    pass
