# coding: utf-8

"""
    Carbon

    Connect external data to LLMs, no matter the source.

    The version of the OpenAPI document: 1.0.0
    Generated by: https://konfigthis.com
"""

from dataclasses import dataclass
import typing_extensions
import urllib3
from pydantic import RootModel
from carbon.request_before_hook import request_before_hook
import json
from urllib3._collections import HTTPHeaderDict

from carbon.api_response import AsyncGeneratorResponse
from carbon import api_client, exceptions
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

from carbon.model.http_validation_error import HTTPValidationError as HTTPValidationErrorSchema
from carbon.model.chunks_and_embeddings_upload_input import ChunksAndEmbeddingsUploadInput as ChunksAndEmbeddingsUploadInputSchema
from carbon.model.chunks_and_embeddings_upload_input_custom_credentials import ChunksAndEmbeddingsUploadInputCustomCredentials as ChunksAndEmbeddingsUploadInputCustomCredentialsSchema
from carbon.model.embedding_generators import EmbeddingGenerators as EmbeddingGeneratorsSchema
from carbon.model.single_chunks_and_embeddings_upload_input import SingleChunksAndEmbeddingsUploadInput as SingleChunksAndEmbeddingsUploadInputSchema
from carbon.model.generic_success_response import GenericSuccessResponse as GenericSuccessResponseSchema

from carbon.type.embedding_generators import EmbeddingGenerators
from carbon.type.http_validation_error import HTTPValidationError
from carbon.type.chunks_and_embeddings_upload_input_custom_credentials import ChunksAndEmbeddingsUploadInputCustomCredentials
from carbon.type.generic_success_response import GenericSuccessResponse
from carbon.type.single_chunks_and_embeddings_upload_input import SingleChunksAndEmbeddingsUploadInput
from carbon.type.chunks_and_embeddings_upload_input import ChunksAndEmbeddingsUploadInput

from ...api_client import Dictionary
from carbon.pydantic.chunks_and_embeddings_upload_input import ChunksAndEmbeddingsUploadInput as ChunksAndEmbeddingsUploadInputPydantic
from carbon.pydantic.http_validation_error import HTTPValidationError as HTTPValidationErrorPydantic
from carbon.pydantic.single_chunks_and_embeddings_upload_input import SingleChunksAndEmbeddingsUploadInput as SingleChunksAndEmbeddingsUploadInputPydantic
from carbon.pydantic.chunks_and_embeddings_upload_input_custom_credentials import ChunksAndEmbeddingsUploadInputCustomCredentials as ChunksAndEmbeddingsUploadInputCustomCredentialsPydantic
from carbon.pydantic.generic_success_response import GenericSuccessResponse as GenericSuccessResponsePydantic
from carbon.pydantic.embedding_generators import EmbeddingGenerators as EmbeddingGeneratorsPydantic

# body param
SchemaForRequestBodyApplicationJson = ChunksAndEmbeddingsUploadInputSchema


request_body_chunks_and_embeddings_upload_input = api_client.RequestBody(
    content={
        'application/json': api_client.MediaType(
            schema=SchemaForRequestBodyApplicationJson),
    },
    required=True,
)
SchemaFor200ResponseBodyApplicationJson = GenericSuccessResponseSchema


@dataclass
class ApiResponseFor200(api_client.ApiResponse):
    body: GenericSuccessResponse


@dataclass
class ApiResponseFor200Async(api_client.AsyncApiResponse):
    body: GenericSuccessResponse


_response_for_200 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor200,
    response_cls_async=ApiResponseFor200Async,
    content={
        'application/json': api_client.MediaType(
            schema=SchemaFor200ResponseBodyApplicationJson),
    },
)
SchemaFor422ResponseBodyApplicationJson = HTTPValidationErrorSchema


@dataclass
class ApiResponseFor422(api_client.ApiResponse):
    body: HTTPValidationError


@dataclass
class ApiResponseFor422Async(api_client.AsyncApiResponse):
    body: HTTPValidationError


_response_for_422 = api_client.OpenApiResponse(
    response_cls=ApiResponseFor422,
    response_cls_async=ApiResponseFor422Async,
    content={
        'application/json': api_client.MediaType(
            schema=SchemaFor422ResponseBodyApplicationJson),
    },
)
_all_accept_content_types = (
    'application/json',
)


class BaseApi(api_client.Api):

    def _upload_chunks_and_embeddings_mapped_args(
        self,
        embedding_model: EmbeddingGenerators,
        chunks_and_embeddings: typing.List[SingleChunksAndEmbeddingsUploadInput],
        overwrite_existing: typing.Optional[bool] = None,
        chunks_only: typing.Optional[bool] = None,
        custom_credentials: typing.Optional[ChunksAndEmbeddingsUploadInputCustomCredentials] = None,
    ) -> api_client.MappedArgs:
        args: api_client.MappedArgs = api_client.MappedArgs()
        _body = {}
        if embedding_model is not None:
            _body["embedding_model"] = embedding_model
        if chunks_and_embeddings is not None:
            _body["chunks_and_embeddings"] = chunks_and_embeddings
        if overwrite_existing is not None:
            _body["overwrite_existing"] = overwrite_existing
        if chunks_only is not None:
            _body["chunks_only"] = chunks_only
        if custom_credentials is not None:
            _body["custom_credentials"] = custom_credentials
        args.body = _body
        return args

    async def _aupload_chunks_and_embeddings_oapg(
        self,
        body: typing.Any = None,
        skip_deserialization: bool = True,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        content_type: str = 'application/json',
        stream: bool = False,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        """
        Upload Chunks And Embeddings
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        used_path = path.value
    
        _headers = HTTPHeaderDict()
        # TODO add cookie handling
        if accept_content_types:
            for accept_content_type in accept_content_types:
                _headers.add('Accept', accept_content_type)
        method = 'post'.upper()
        _headers.add('Content-Type', content_type)
    
        if body is schemas.unset:
            raise exceptions.ApiValueError(
                'The required body parameter has an invalid value of: unset. Set a valid value instead')
        _fields = None
        _body = None
        request_before_hook(
            resource_path=used_path,
            method=method,
            configuration=self.api_client.configuration,
            path_template='/upload_chunks_and_embeddings',
            body=body,
            auth_settings=_auth,
            headers=_headers,
        )
        serialized_data = request_body_chunks_and_embeddings_upload_input.serialize(body, content_type)
        if 'fields' in serialized_data:
            _fields = serialized_data['fields']
        elif 'body' in serialized_data:
            _body = serialized_data['body']
    
        response = await self.api_client.async_call_api(
            resource_path=used_path,
            method=method,
            headers=_headers,
            fields=_fields,
            serialized_body=_body,
            body=body,
            auth_settings=_auth,
            timeout=timeout,
            **kwargs
        )
    
        if stream:
            if not 200 <= response.http_response.status <= 299:
                body = (await response.http_response.content.read()).decode("utf-8")
                raise exceptions.ApiStreamingException(
                    status=response.http_response.status,
                    reason=response.http_response.reason,
                    body=body,
                )
    
            async def stream_iterator():
                """
                iterates over response.http_response.content and closes connection once iteration has finished
                """
                async for line in response.http_response.content:
                    if line == b'\r\n':
                        continue
                    yield line
                response.http_response.close()
                await response.session.close()
            return AsyncGeneratorResponse(
                content=stream_iterator(),
                headers=response.http_response.headers,
                status=response.http_response.status,
                response=response.http_response
            )
    
        response_for_status = _status_code_to_response.get(str(response.http_response.status))
        if response_for_status:
            api_response = await response_for_status.deserialize_async(
                                                    response,
                                                    self.api_client.configuration,
                                                    skip_deserialization=skip_deserialization
                                                )
        else:
            # If response data is JSON then deserialize for SDK consumer convenience
            is_json = api_client.JSONDetector._content_type_is_json(response.http_response.headers.get('Content-Type', ''))
            api_response = api_client.ApiResponseWithoutDeserializationAsync(
                body=await response.http_response.json() if is_json else await response.http_response.text(),
                response=response.http_response,
                round_trip_time=response.round_trip_time,
                status=response.http_response.status,
                headers=response.http_response.headers,
            )
    
        if not 200 <= api_response.status <= 299:
            raise exceptions.ApiException(api_response=api_response)
    
        # cleanup session / response
        response.http_response.close()
        await response.session.close()
    
        return api_response


    def _upload_chunks_and_embeddings_oapg(
        self,
        body: typing.Any = None,
        skip_deserialization: bool = True,
        timeout: typing.Optional[typing.Union[float, typing.Tuple]] = None,
        accept_content_types: typing.Tuple[str] = _all_accept_content_types,
        content_type: str = 'application/json',
        stream: bool = False,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """
        Upload Chunks And Embeddings
        :param skip_deserialization: If true then api_response.response will be set but
            api_response.body and api_response.headers will not be deserialized into schema
            class instances
        """
        used_path = path.value
    
        _headers = HTTPHeaderDict()
        # TODO add cookie handling
        if accept_content_types:
            for accept_content_type in accept_content_types:
                _headers.add('Accept', accept_content_type)
        method = 'post'.upper()
        _headers.add('Content-Type', content_type)
    
        if body is schemas.unset:
            raise exceptions.ApiValueError(
                'The required body parameter has an invalid value of: unset. Set a valid value instead')
        _fields = None
        _body = None
        request_before_hook(
            resource_path=used_path,
            method=method,
            configuration=self.api_client.configuration,
            path_template='/upload_chunks_and_embeddings',
            body=body,
            auth_settings=_auth,
            headers=_headers,
        )
        serialized_data = request_body_chunks_and_embeddings_upload_input.serialize(body, content_type)
        if 'fields' in serialized_data:
            _fields = serialized_data['fields']
        elif 'body' in serialized_data:
            _body = serialized_data['body']
    
        response = self.api_client.call_api(
            resource_path=used_path,
            method=method,
            headers=_headers,
            fields=_fields,
            serialized_body=_body,
            body=body,
            auth_settings=_auth,
            timeout=timeout,
        )
    
        response_for_status = _status_code_to_response.get(str(response.http_response.status))
        if response_for_status:
            api_response = response_for_status.deserialize(
                                                    response,
                                                    self.api_client.configuration,
                                                    skip_deserialization=skip_deserialization
                                                )
        else:
            # If response data is JSON then deserialize for SDK consumer convenience
            is_json = api_client.JSONDetector._content_type_is_json(response.http_response.headers.get('Content-Type', ''))
            api_response = api_client.ApiResponseWithoutDeserialization(
                body=json.loads(response.http_response.data) if is_json else response.http_response.data,
                response=response.http_response,
                round_trip_time=response.round_trip_time,
                status=response.http_response.status,
                headers=response.http_response.headers,
            )
    
        if not 200 <= api_response.status <= 299:
            raise exceptions.ApiException(api_response=api_response)
    
        return api_response


class UploadChunksAndEmbeddingsRaw(BaseApi):
    # this class is used by api classes that refer to endpoints with operationId fn names

    async def aupload_chunks_and_embeddings(
        self,
        embedding_model: EmbeddingGenerators,
        chunks_and_embeddings: typing.List[SingleChunksAndEmbeddingsUploadInput],
        overwrite_existing: typing.Optional[bool] = None,
        chunks_only: typing.Optional[bool] = None,
        custom_credentials: typing.Optional[ChunksAndEmbeddingsUploadInputCustomCredentials] = None,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._upload_chunks_and_embeddings_mapped_args(
            embedding_model=embedding_model,
            chunks_and_embeddings=chunks_and_embeddings,
            overwrite_existing=overwrite_existing,
            chunks_only=chunks_only,
            custom_credentials=custom_credentials,
        )
        return await self._aupload_chunks_and_embeddings_oapg(
            body=args.body,
            **kwargs,
        )
    
    def upload_chunks_and_embeddings(
        self,
        embedding_model: EmbeddingGenerators,
        chunks_and_embeddings: typing.List[SingleChunksAndEmbeddingsUploadInput],
        overwrite_existing: typing.Optional[bool] = None,
        chunks_only: typing.Optional[bool] = None,
        custom_credentials: typing.Optional[ChunksAndEmbeddingsUploadInputCustomCredentials] = None,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """  """
        args = self._upload_chunks_and_embeddings_mapped_args(
            embedding_model=embedding_model,
            chunks_and_embeddings=chunks_and_embeddings,
            overwrite_existing=overwrite_existing,
            chunks_only=chunks_only,
            custom_credentials=custom_credentials,
        )
        return self._upload_chunks_and_embeddings_oapg(
            body=args.body,
        )

class UploadChunksAndEmbeddings(BaseApi):

    async def aupload_chunks_and_embeddings(
        self,
        embedding_model: EmbeddingGenerators,
        chunks_and_embeddings: typing.List[SingleChunksAndEmbeddingsUploadInput],
        overwrite_existing: typing.Optional[bool] = None,
        chunks_only: typing.Optional[bool] = None,
        custom_credentials: typing.Optional[ChunksAndEmbeddingsUploadInputCustomCredentials] = None,
        validate: bool = False,
        **kwargs,
    ) -> GenericSuccessResponsePydantic:
        raw_response = await self.raw.aupload_chunks_and_embeddings(
            embedding_model=embedding_model,
            chunks_and_embeddings=chunks_and_embeddings,
            overwrite_existing=overwrite_existing,
            chunks_only=chunks_only,
            custom_credentials=custom_credentials,
            **kwargs,
        )
        if validate:
            return GenericSuccessResponsePydantic(**raw_response.body)
        return api_client.construct_model_instance(GenericSuccessResponsePydantic, raw_response.body)
    
    
    def upload_chunks_and_embeddings(
        self,
        embedding_model: EmbeddingGenerators,
        chunks_and_embeddings: typing.List[SingleChunksAndEmbeddingsUploadInput],
        overwrite_existing: typing.Optional[bool] = None,
        chunks_only: typing.Optional[bool] = None,
        custom_credentials: typing.Optional[ChunksAndEmbeddingsUploadInputCustomCredentials] = None,
        validate: bool = False,
    ) -> GenericSuccessResponsePydantic:
        raw_response = self.raw.upload_chunks_and_embeddings(
            embedding_model=embedding_model,
            chunks_and_embeddings=chunks_and_embeddings,
            overwrite_existing=overwrite_existing,
            chunks_only=chunks_only,
            custom_credentials=custom_credentials,
        )
        if validate:
            return GenericSuccessResponsePydantic(**raw_response.body)
        return api_client.construct_model_instance(GenericSuccessResponsePydantic, raw_response.body)


class ApiForpost(BaseApi):
    # this class is used by api classes that refer to endpoints by path and http method names

    async def apost(
        self,
        embedding_model: EmbeddingGenerators,
        chunks_and_embeddings: typing.List[SingleChunksAndEmbeddingsUploadInput],
        overwrite_existing: typing.Optional[bool] = None,
        chunks_only: typing.Optional[bool] = None,
        custom_credentials: typing.Optional[ChunksAndEmbeddingsUploadInputCustomCredentials] = None,
        **kwargs,
    ) -> typing.Union[
        ApiResponseFor200Async,
        api_client.ApiResponseWithoutDeserializationAsync,
        AsyncGeneratorResponse,
    ]:
        args = self._upload_chunks_and_embeddings_mapped_args(
            embedding_model=embedding_model,
            chunks_and_embeddings=chunks_and_embeddings,
            overwrite_existing=overwrite_existing,
            chunks_only=chunks_only,
            custom_credentials=custom_credentials,
        )
        return await self._aupload_chunks_and_embeddings_oapg(
            body=args.body,
            **kwargs,
        )
    
    def post(
        self,
        embedding_model: EmbeddingGenerators,
        chunks_and_embeddings: typing.List[SingleChunksAndEmbeddingsUploadInput],
        overwrite_existing: typing.Optional[bool] = None,
        chunks_only: typing.Optional[bool] = None,
        custom_credentials: typing.Optional[ChunksAndEmbeddingsUploadInputCustomCredentials] = None,
    ) -> typing.Union[
        ApiResponseFor200,
        api_client.ApiResponseWithoutDeserialization,
    ]:
        """  """
        args = self._upload_chunks_and_embeddings_mapped_args(
            embedding_model=embedding_model,
            chunks_and_embeddings=chunks_and_embeddings,
            overwrite_existing=overwrite_existing,
            chunks_only=chunks_only,
            custom_credentials=custom_credentials,
        )
        return self._upload_chunks_and_embeddings_oapg(
            body=args.body,
        )

