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

from carbon.pydantic.embedding_generators_nullable import EmbeddingGeneratorsNullable
from carbon.pydantic.file_sync_config_nullable import FileSyncConfigNullable

class FreshDeskConnectRequest(BaseModel):
    domain: str = Field(alias='domain')

    api_key: str = Field(alias='api_key')

    tags: typing.Optional[typing.Optional[typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]]] = Field(None, alias='tags')

    chunk_size: typing.Optional[typing.Optional[int]] = Field(None, alias='chunk_size')

    chunk_overlap: typing.Optional[typing.Optional[int]] = Field(None, alias='chunk_overlap')

    skip_embedding_generation: typing.Optional[typing.Optional[bool]] = Field(None, alias='skip_embedding_generation')

    embedding_model: typing.Optional[EmbeddingGeneratorsNullable] = Field(None, alias='embedding_model')

    generate_sparse_vectors: typing.Optional[typing.Optional[bool]] = Field(None, alias='generate_sparse_vectors')

    prepend_filename_to_chunks: typing.Optional[typing.Optional[bool]] = Field(None, alias='prepend_filename_to_chunks')

    sync_files_on_connection: typing.Optional[typing.Optional[bool]] = Field(None, alias='sync_files_on_connection')

    request_id: typing.Optional[typing.Optional[str]] = Field(None, alias='request_id')

    # Enabling this flag will fetch all available content from the source to be listed via list items endpoint
    sync_source_items: typing.Optional[bool] = Field(None, alias='sync_source_items')

    file_sync_config: typing.Optional[FileSyncConfigNullable] = Field(None, alias='file_sync_config')

    model_config = ConfigDict(
        protected_namespaces=(),
        arbitrary_types_allowed=True
    )
