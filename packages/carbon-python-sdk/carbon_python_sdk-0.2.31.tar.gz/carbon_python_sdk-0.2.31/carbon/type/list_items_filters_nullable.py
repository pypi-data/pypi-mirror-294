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

from carbon.type.list_items_filters_nullable_external_ids import ListItemsFiltersNullableExternalIds
from carbon.type.list_items_filters_nullable_ids import ListItemsFiltersNullableIds

class RequiredListItemsFiltersNullable(TypedDict):
    pass

class OptionalListItemsFiltersNullable(TypedDict, total=False):
    external_ids: typing.Optional[ListItemsFiltersNullableExternalIds]

    ids: typing.Optional[ListItemsFiltersNullableIds]

    name: typing.Optional[str]

    root_files_only: typing.Optional[bool]

class ListItemsFiltersNullable(RequiredListItemsFiltersNullable, OptionalListItemsFiltersNullable):
    pass
