from typing import List, Optional, Union
from truvity_sdk.client import AsyncTruvityApi, TruvityApi
from truvity_sdk.documents.credentials.base_verifiable_credential import AsyncBaseVerifiableCredential, BaseVerifiableCredential
from truvity_sdk.documents.credentials.issued import AsyncVerifiableCredential, VerifiableCredential
from truvity_sdk.documents.credentials.unknown import AsyncUnknownVerifiableCredential, UnknownVerifiableCredential
from truvity_sdk.documents.helpers import generate_idempotency_key
from truvity_sdk.documents.presentations.issued import AsyncVerifiablePresentation, VerifiablePresentation, issue, issue_async
from truvity_sdk.documents.types import PresentationDescriptor, UpdatePayload
from truvity_sdk.types.credential_resource import CredentialResource

Credentials = Union[
    List[str],
    List[VerifiableCredential],
    List[UnknownVerifiableCredential],
    List[BaseVerifiableCredential],
    List[CredentialResource],
    List[AsyncVerifiableCredential],
    List[AsyncUnknownVerifiableCredential],
    List[AsyncBaseVerifiableCredential]
]

def _credential_ids(
        credentials: Credentials
    ) -> List[str]:
    return [
        item if isinstance(item, str)
        else item.descriptor.id if isinstance(item, BaseVerifiableCredential) or isinstance(item, AsyncBaseVerifiableCredential)
        else item.id
        for item in credentials
    ]

class VpDecorator:
    def __init__(self, client: TruvityApi):
        self.client = client

    def issue(
        self,
        credentials: Credentials,
        private_key_id: str
    ) -> VerifiablePresentation:
        return issue(
            self.client,
            _credential_ids(credentials),
            private_key_id
        )

    def load(self, id: str, revision: Optional[int] = None) -> VerifiablePresentation:
        if revision is None:
            presentation_resource = self.client.presentations.presentation_latest(id)
        else:
            presentation_resource = self.client.presentations.presentation_revision(id, revision)

        return VerifiablePresentation(
            self.client,
            PresentationDescriptor.from_presentation_resource(presentation_resource)
        )

    def import_presentation(self, blob: bytes, request: Optional[UpdatePayload] = None) -> VerifiablePresentation:
        idempotency_key = generate_idempotency_key('importBlob')
        upload_details = self.client.presentations.presentation_upload(
            idempotency_key=idempotency_key,
        )

        self.client._client_wrapper.httpx_client.request(
            upload_details.upload_uri,
            method='PUT',
            content=blob,
        ).raise_for_status()

        presentation_resource = self.client.presentations.presentation_import(
            blob_id=upload_details.blob_id,
            annotations=request.annotations if request is not None else None,
            labels=request.labels if request is not None else None,
            idempotency_key=idempotency_key,
        )

        return VerifiablePresentation(
            self.client,
            PresentationDescriptor.from_presentation_resource(presentation_resource)
        )

class AsyncVpDecorator:
    def __init__(self, client: AsyncTruvityApi):
        self.client = client

    async def issue(
        self,
        credentials: Credentials,
        private_key_id: str
    ) -> AsyncVerifiablePresentation:
        return await issue_async(
            self.client,
            _credential_ids(credentials),
            private_key_id
        )

    async def load(self, id: str, revision: Optional[int] = None) -> AsyncVerifiablePresentation:
        if revision is None:
            presentation_resource = await self.client.presentations.presentation_latest(id)
        else:
            presentation_resource = await self.client.presentations.presentation_revision(id, revision)

        return AsyncVerifiablePresentation(
            self.client,
            PresentationDescriptor.from_presentation_resource(presentation_resource)
        )

    async def import_presentation(self, blob: bytes, request: Optional[UpdatePayload] = None) -> AsyncVerifiablePresentation:
        idempotency_key = generate_idempotency_key('importBlob')
        upload_details = await self.client.presentations.presentation_upload(
            idempotency_key=idempotency_key,
        )

        (await self.client._client_wrapper.httpx_client.request(
            upload_details.upload_uri,
            method='PUT',
            content=blob,
        )).raise_for_status()

        presentation_resource = await self.client.presentations.presentation_import(
            blob_id=upload_details.blob_id,
            annotations=request.annotations if request is not None else None,
            labels=request.labels if request is not None else None,
            idempotency_key=idempotency_key,
        )

        return AsyncVerifiablePresentation(
            self.client,
            PresentationDescriptor.from_presentation_resource(presentation_resource)
        )
