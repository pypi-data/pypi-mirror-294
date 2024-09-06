from dataclasses import dataclass
from typing import Dict, Generic, Optional, Type, TypeVar, Union, cast, overload

from truvity_sdk.client import AsyncTruvityApi, TruvityApi
from truvity_sdk.documents.credentials.draft import AsyncDraftCredential, DraftCredential
from truvity_sdk.documents.credentials.flavor import CredentialFlavor
from truvity_sdk.documents.credentials.issued import AsyncVerifiableCredential, VerifiableCredential
from truvity_sdk.documents.credentials.map import map_async, map_sync
from truvity_sdk.documents.document_model import DocumentModel, LinkedCredential
from truvity_sdk.documents.helpers import generate_idempotency_key
from truvity_sdk.documents.types import CredentialBlob, CredentialDescriptor, DraftDataDescriptor, UpdatePayload
from truvity_sdk.errors.not_found_error import NotFoundError
from truvity_sdk.types.credential_resource import CredentialResource
from truvity_sdk.types.draft import Draft
from truvity_sdk.types.draft_resource import DraftResource

T = TypeVar("T", bound=DocumentModel)

class LoadedCredential(Generic[T]):
    def __init__(self, credential: Union[DraftCredential[T], VerifiableCredential[T]]) -> None:
        self.credential = credential

    def is_verifiable(self):
        return isinstance(self.credential, VerifiableCredential)

class AsyncLoadedCredential(Generic[T]):
    def __init__(self, credential: Union[AsyncDraftCredential[T], AsyncVerifiableCredential[T]]) -> None:
        self.credential = credential

    def is_verifiable(self):
        return isinstance(self.credential, AsyncVerifiableCredential)

class VcDecorator(Generic[T]):
    def __init__(self, client: TruvityApi, model: Type[T]) -> None:
        self.flavor = CredentialFlavor(model)
        self.client = client
        self.model = model

    @overload
    def map(self, input: CredentialResource) -> VerifiableCredential[T]: ...
    @overload
    def map(self, input: DraftResource) -> DraftCredential[T]: ...

    def map(self, input: Union[DraftResource, CredentialResource]) -> Union[VerifiableCredential[T], DraftCredential[T]]:
        return map_sync(self.model, self.client, input)

    def create(self, claims: Optional[T] = None, request: Optional[UpdatePayload] = None)-> DraftCredential[T]:
        data = Draft(
                schema=self.model.draft_schema(),
                values=claims.to_api_values() if claims is not None else None
        )
        draft_resource = self.client.drafts.draft_create(
            data=data,
            annotations=request.annotations if request is not None else None,
            labels=request.labels if request is not None else None,
            idempotency_key=generate_idempotency_key("create"),
        )
        return DraftCredential(
            self.client,
            self.flavor,
            DraftDataDescriptor.from_resource(draft_resource),
            CredentialDescriptor.from_resource(draft_resource)
        )

    def load_as_draft(self, id: str, revision: Optional[int] = None) -> DraftCredential[T]:
        if revision is None:
            draft_resource = self.client.drafts.draft_latest(id)
        else:
            draft_resource = self.client.drafts.draft_revision(id, revision)
        return self.map(draft_resource)

    def load_as_credential(self, id: str, revision: Optional[int] = None) -> VerifiableCredential[T]:
        if revision is None:
            credential_resource = self.client.credentials.credential_latest(id)
        else:
            credential_resource = self.client.credentials.credential_revision(id, revision)
        return self.map(credential_resource)

    def load(self, id: str, revision: Optional[int] = None) -> LoadedCredential[T]:
        verifiable_credential: Optional[VerifiableCredential[T]] = None
        draft_credential: Optional[DraftCredential[T]] = None

        try:
            verifiable_credential = self.load_as_credential(id, revision)
        except NotFoundError:
            draft_credential = self.load_as_draft(id, revision)

        if draft_credential is None:
            if verifiable_credential is None:
                raise Exception(f"Resource with id '{id}' could not be found.")

            return LoadedCredential(
                credential=verifiable_credential,
            )
        else:
            return LoadedCredential(
                credential=draft_credential,
            )

    def __import_blob(self, blob: CredentialBlob, request: Optional[UpdatePayload]) -> CredentialDescriptor:
        idempotency_key = generate_idempotency_key("importBlob")
        credential_upload_result = self.client.credentials.credential_upload(
            idempotency_key=idempotency_key,
        )

        self.client._client_wrapper.httpx_client.request(
            credential_upload_result.upload_uri,
            method="PUT",
            data=blob
        ).raise_for_status()

        credential_resource = self.client.credentials.credential_import(
            annotations=request.annotations if request is not None else None,
            labels=request.labels if request is not None else None,
            blob_id=credential_upload_result.blob_id,
            idempotency_key=idempotency_key,
        )

        return CredentialDescriptor.from_resource(credential_resource)

    def import_credential(self, blob: CredentialBlob, request: Optional[UpdatePayload] = None) -> VerifiableCredential[T]:
        credential =  self.__import_blob(blob, request)

        return VerifiableCredential(self.client, self.flavor, credential, blob)

    def dereference(self, linked_credential: LinkedCredential[T]) -> VerifiableCredential[T]:
        loaded_credential = self.load(linked_credential.id)

        # TODO: add support for working with both issued and draft creds
        if not loaded_credential.is_verifiable():
            raise Exception(f"The linked credential is not a VC: {linked_credential.id}")

        return cast(VerifiableCredential[T], loaded_credential.credential)

class AsyncVcDecorator(Generic[T]):
    def __init__(self, client: AsyncTruvityApi, model: Type[T]) -> None:
        self.flavor = CredentialFlavor(model)
        self.client = client
        self.model = model

    @overload
    def map(self, input: CredentialResource) -> AsyncVerifiableCredential[T]: ...
    @overload
    def map(self, input: DraftResource) -> AsyncDraftCredential[T]: ...

    def map(self, input: Union[DraftResource, CredentialResource]) -> Union[AsyncVerifiableCredential[T], AsyncDraftCredential[T]]:
        return map_async(self.model, self.client, input)

    async def create(self, claims: Optional[T] = None, request: Optional[UpdatePayload] = None)-> AsyncDraftCredential[T]:
        draft_resource = await self.client.drafts.draft_create(
            data=Draft(
                schema=self.model.draft_schema(),
                values=claims.to_api_values() if claims is not None else None
            ),
            annotations=request.annotations if request is not None else None,
            labels=request.labels if request is not None else None,
            idempotency_key=generate_idempotency_key("create"),
        )
        return AsyncDraftCredential(
            self.client,
            self.flavor,
            DraftDataDescriptor.from_resource(draft_resource),
            CredentialDescriptor.from_resource(draft_resource)
        )

    async def load_as_draft(self, id: str, revision: Optional[int] = None) -> AsyncDraftCredential[T]:
        if revision is None:
            draft_resource = await self.client.drafts.draft_latest(id)
        else:
            draft_resource = await self.client.drafts.draft_revision(id, revision)
        return self.map(draft_resource)

    async def load_as_credential(self, id: str, revision: Optional[int] = None) -> AsyncVerifiableCredential[T]:
        if revision is None:
            credential_resource = await self.client.credentials.credential_latest(id)
        else:
            credential_resource = await self.client.credentials.credential_revision(id, revision)
        return self.map(credential_resource)

    async def load(self, id: str, revision: Optional[int] = None) -> AsyncLoadedCredential[T]:
        verifiable_credential: Optional[AsyncVerifiableCredential[T]] = None
        draft_credential: Optional[AsyncDraftCredential[T]] = None

        try:
            verifiable_credential = await self.load_as_credential(id, revision)
        except NotFoundError:
            draft_credential = await self.load_as_draft(id, revision)

        if draft_credential is None:
            if verifiable_credential is None:
                raise Exception(f"Resource with id '{id}' could not be found.")

            return AsyncLoadedCredential(
                credential=verifiable_credential,
            )
        else:
            return AsyncLoadedCredential(
                credential=draft_credential,
            )

    async def __import_blob(self, blob: CredentialBlob, request: Optional[UpdatePayload]) -> CredentialDescriptor:
        idempotency_key = generate_idempotency_key("importBlob")
        credential_upload_result = await self.client.credentials.credential_upload(
            idempotency_key=idempotency_key,
        )

        (await self.client._client_wrapper.httpx_client.request(
            credential_upload_result.upload_uri,
            method="PUT",
            data=blob
        )).raise_for_status()

        credential_resource = await self.client.credentials.credential_import(
            annotations=request.annotations if request is not None else None,
            labels=request.labels if request is not None else None,
            blob_id=credential_upload_result.blob_id,
            idempotency_key=idempotency_key,
        )

        return CredentialDescriptor.from_resource(credential_resource)

    async def import_credential(self, blob: CredentialBlob, request: Optional[UpdatePayload] = None) -> AsyncVerifiableCredential[T]:
        credential = await self.__import_blob(blob, request)

        return AsyncVerifiableCredential(self.client, self.flavor, credential, blob)

    async def dereference(self, linked_credential: LinkedCredential[T]) -> AsyncVerifiableCredential[T]:
        loaded_credential = await self.load(linked_credential.id)

        # TODO: add support for working with both issued and draft creds
        if not loaded_credential.is_verifiable():
            raise Exception(f"The linked credential is not a VC: {linked_credential.id}")

        return cast(AsyncVerifiableCredential[T], loaded_credential.credential)
