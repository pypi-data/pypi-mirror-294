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

from carbon.type.organization_user_files_to_sync_filters import OrganizationUserFilesToSyncFilters

class RequiredModifyColdStorageParametersQueryInput(TypedDict):
    pass

class OptionalModifyColdStorageParametersQueryInput(TypedDict, total=False):
    filters: OrganizationUserFilesToSyncFilters

    enable_cold_storage: typing.Optional[bool]

    hot_storage_time_to_live: typing.Optional[int]

class ModifyColdStorageParametersQueryInput(RequiredModifyColdStorageParametersQueryInput, OptionalModifyColdStorageParametersQueryInput):
    pass
