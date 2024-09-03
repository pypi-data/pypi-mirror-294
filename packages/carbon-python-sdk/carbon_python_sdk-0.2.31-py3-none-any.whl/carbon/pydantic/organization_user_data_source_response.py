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
from pydantic import BaseModel, Field, RootModel, ConfigDict

from carbon.pydantic.organization_user_data_source_api import OrganizationUserDataSourceAPI

class OrganizationUserDataSourceResponse(BaseModel):
    results: typing.List[OrganizationUserDataSourceAPI] = Field(alias='results')

    count: int = Field(alias='count')

    model_config = ConfigDict(
        protected_namespaces=(),
        arbitrary_types_allowed=True
    )
