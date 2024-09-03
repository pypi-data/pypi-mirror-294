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


ExternalFileSyncStatuses = Literal["DELAYED", "QUEUED_FOR_SYNC", "SYNCING", "READY", "SYNC_ERROR", "EVALUATING_RESYNC", "RATE_LIMITED", "SYNC_ABORTED", "QUEUED_FOR_OCR"]
