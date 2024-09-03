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


class RequiredResyncFileQueryInput(TypedDict):
    file_id: int


class OptionalResyncFileQueryInput(TypedDict, total=False):
    chunk_size: typing.Optional[int]

    chunk_overlap: typing.Optional[int]

    force_embedding_generation: bool

class ResyncFileQueryInput(RequiredResyncFileQueryInput, OptionalResyncFileQueryInput):
    pass
