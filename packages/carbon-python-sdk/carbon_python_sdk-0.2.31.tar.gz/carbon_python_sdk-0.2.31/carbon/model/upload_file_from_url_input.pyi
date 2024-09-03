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


class UploadFileFromUrlInput(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        required = {
            "url",
        }
        
        class properties:
            url = schemas.StrSchema
            
            
            class file_name(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'file_name':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class chunk_size(
                schemas.IntBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'chunk_size':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            
            
            class chunk_overlap(
                schemas.IntBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'chunk_overlap':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            skip_embedding_generation = schemas.BoolSchema
            set_page_as_boundary = schemas.BoolSchema
        
            @staticmethod
            def embedding_model() -> typing.Type['EmbeddingGenerators']:
                return EmbeddingGenerators
            generate_sparse_vectors = schemas.BoolSchema
            use_textract = schemas.BoolSchema
            prepend_filename_to_chunks = schemas.BoolSchema
            
            
            class max_items_per_chunk(
                schemas.IntBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneDecimalMixin
            ):
            
            
                def __new__(
                    cls,
                    *args: typing.Union[None, decimal.Decimal, int, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'max_items_per_chunk':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                    )
            parse_pdf_tables_with_ocr = schemas.BoolSchema
            detect_audio_language = schemas.BoolSchema
        
            @staticmethod
            def transcription_service() -> typing.Type['TranscriptionServiceNullable']:
                return TranscriptionServiceNullable
            include_speaker_labels = schemas.BoolSchema
        
            @staticmethod
            def media_type() -> typing.Type['FileContentTypesNullable']:
                return FileContentTypesNullable
            split_rows = schemas.BoolSchema
        
            @staticmethod
            def cold_storage_params() -> typing.Type['ColdStorageProps']:
                return ColdStorageProps
            __annotations__ = {
                "url": url,
                "file_name": file_name,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "skip_embedding_generation": skip_embedding_generation,
                "set_page_as_boundary": set_page_as_boundary,
                "embedding_model": embedding_model,
                "generate_sparse_vectors": generate_sparse_vectors,
                "use_textract": use_textract,
                "prepend_filename_to_chunks": prepend_filename_to_chunks,
                "max_items_per_chunk": max_items_per_chunk,
                "parse_pdf_tables_with_ocr": parse_pdf_tables_with_ocr,
                "detect_audio_language": detect_audio_language,
                "transcription_service": transcription_service,
                "include_speaker_labels": include_speaker_labels,
                "media_type": media_type,
                "split_rows": split_rows,
                "cold_storage_params": cold_storage_params,
            }
    
    url: MetaOapg.properties.url
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["url"]) -> MetaOapg.properties.url: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["file_name"]) -> MetaOapg.properties.file_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["chunk_size"]) -> MetaOapg.properties.chunk_size: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["chunk_overlap"]) -> MetaOapg.properties.chunk_overlap: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["skip_embedding_generation"]) -> MetaOapg.properties.skip_embedding_generation: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["set_page_as_boundary"]) -> MetaOapg.properties.set_page_as_boundary: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["embedding_model"]) -> 'EmbeddingGenerators': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["generate_sparse_vectors"]) -> MetaOapg.properties.generate_sparse_vectors: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["use_textract"]) -> MetaOapg.properties.use_textract: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["prepend_filename_to_chunks"]) -> MetaOapg.properties.prepend_filename_to_chunks: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_items_per_chunk"]) -> MetaOapg.properties.max_items_per_chunk: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["parse_pdf_tables_with_ocr"]) -> MetaOapg.properties.parse_pdf_tables_with_ocr: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["detect_audio_language"]) -> MetaOapg.properties.detect_audio_language: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["transcription_service"]) -> 'TranscriptionServiceNullable': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["include_speaker_labels"]) -> MetaOapg.properties.include_speaker_labels: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["media_type"]) -> 'FileContentTypesNullable': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["split_rows"]) -> MetaOapg.properties.split_rows: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["cold_storage_params"]) -> 'ColdStorageProps': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["url", "file_name", "chunk_size", "chunk_overlap", "skip_embedding_generation", "set_page_as_boundary", "embedding_model", "generate_sparse_vectors", "use_textract", "prepend_filename_to_chunks", "max_items_per_chunk", "parse_pdf_tables_with_ocr", "detect_audio_language", "transcription_service", "include_speaker_labels", "media_type", "split_rows", "cold_storage_params", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["url"]) -> MetaOapg.properties.url: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["file_name"]) -> typing.Union[MetaOapg.properties.file_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["chunk_size"]) -> typing.Union[MetaOapg.properties.chunk_size, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["chunk_overlap"]) -> typing.Union[MetaOapg.properties.chunk_overlap, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["skip_embedding_generation"]) -> typing.Union[MetaOapg.properties.skip_embedding_generation, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["set_page_as_boundary"]) -> typing.Union[MetaOapg.properties.set_page_as_boundary, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["embedding_model"]) -> typing.Union['EmbeddingGenerators', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["generate_sparse_vectors"]) -> typing.Union[MetaOapg.properties.generate_sparse_vectors, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["use_textract"]) -> typing.Union[MetaOapg.properties.use_textract, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["prepend_filename_to_chunks"]) -> typing.Union[MetaOapg.properties.prepend_filename_to_chunks, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_items_per_chunk"]) -> typing.Union[MetaOapg.properties.max_items_per_chunk, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["parse_pdf_tables_with_ocr"]) -> typing.Union[MetaOapg.properties.parse_pdf_tables_with_ocr, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["detect_audio_language"]) -> typing.Union[MetaOapg.properties.detect_audio_language, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["transcription_service"]) -> typing.Union['TranscriptionServiceNullable', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["include_speaker_labels"]) -> typing.Union[MetaOapg.properties.include_speaker_labels, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["media_type"]) -> typing.Union['FileContentTypesNullable', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["split_rows"]) -> typing.Union[MetaOapg.properties.split_rows, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["cold_storage_params"]) -> typing.Union['ColdStorageProps', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["url", "file_name", "chunk_size", "chunk_overlap", "skip_embedding_generation", "set_page_as_boundary", "embedding_model", "generate_sparse_vectors", "use_textract", "prepend_filename_to_chunks", "max_items_per_chunk", "parse_pdf_tables_with_ocr", "detect_audio_language", "transcription_service", "include_speaker_labels", "media_type", "split_rows", "cold_storage_params", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        url: typing.Union[MetaOapg.properties.url, str, ],
        file_name: typing.Union[MetaOapg.properties.file_name, None, str, schemas.Unset] = schemas.unset,
        chunk_size: typing.Union[MetaOapg.properties.chunk_size, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        chunk_overlap: typing.Union[MetaOapg.properties.chunk_overlap, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        skip_embedding_generation: typing.Union[MetaOapg.properties.skip_embedding_generation, bool, schemas.Unset] = schemas.unset,
        set_page_as_boundary: typing.Union[MetaOapg.properties.set_page_as_boundary, bool, schemas.Unset] = schemas.unset,
        embedding_model: typing.Union['EmbeddingGenerators', schemas.Unset] = schemas.unset,
        generate_sparse_vectors: typing.Union[MetaOapg.properties.generate_sparse_vectors, bool, schemas.Unset] = schemas.unset,
        use_textract: typing.Union[MetaOapg.properties.use_textract, bool, schemas.Unset] = schemas.unset,
        prepend_filename_to_chunks: typing.Union[MetaOapg.properties.prepend_filename_to_chunks, bool, schemas.Unset] = schemas.unset,
        max_items_per_chunk: typing.Union[MetaOapg.properties.max_items_per_chunk, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        parse_pdf_tables_with_ocr: typing.Union[MetaOapg.properties.parse_pdf_tables_with_ocr, bool, schemas.Unset] = schemas.unset,
        detect_audio_language: typing.Union[MetaOapg.properties.detect_audio_language, bool, schemas.Unset] = schemas.unset,
        transcription_service: typing.Union['TranscriptionServiceNullable', schemas.Unset] = schemas.unset,
        include_speaker_labels: typing.Union[MetaOapg.properties.include_speaker_labels, bool, schemas.Unset] = schemas.unset,
        media_type: typing.Union['FileContentTypesNullable', schemas.Unset] = schemas.unset,
        split_rows: typing.Union[MetaOapg.properties.split_rows, bool, schemas.Unset] = schemas.unset,
        cold_storage_params: typing.Union['ColdStorageProps', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'UploadFileFromUrlInput':
        return super().__new__(
            cls,
            *args,
            url=url,
            file_name=file_name,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            skip_embedding_generation=skip_embedding_generation,
            set_page_as_boundary=set_page_as_boundary,
            embedding_model=embedding_model,
            generate_sparse_vectors=generate_sparse_vectors,
            use_textract=use_textract,
            prepend_filename_to_chunks=prepend_filename_to_chunks,
            max_items_per_chunk=max_items_per_chunk,
            parse_pdf_tables_with_ocr=parse_pdf_tables_with_ocr,
            detect_audio_language=detect_audio_language,
            transcription_service=transcription_service,
            include_speaker_labels=include_speaker_labels,
            media_type=media_type,
            split_rows=split_rows,
            cold_storage_params=cold_storage_params,
            _configuration=_configuration,
            **kwargs,
        )

from carbon.model.cold_storage_props import ColdStorageProps
from carbon.model.embedding_generators import EmbeddingGenerators
from carbon.model.file_content_types_nullable import FileContentTypesNullable
from carbon.model.transcription_service_nullable import TranscriptionServiceNullable
