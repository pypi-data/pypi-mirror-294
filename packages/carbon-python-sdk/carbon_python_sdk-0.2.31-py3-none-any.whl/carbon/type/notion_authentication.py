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


class RequiredNotionAuthentication(TypedDict):
    source: typing.Union[bool, date, datetime, dict, float, int, list, str, None]

    access_token: str

    workspace_id: str

class OptionalNotionAuthentication(TypedDict, total=False):
    pass

class NotionAuthentication(RequiredNotionAuthentication, OptionalNotionAuthentication):
    pass
