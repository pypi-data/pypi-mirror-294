from typing import Optional

from truvity_sdk.client import AsyncTruvityApi, TruvityApi
from truvity_sdk.documents.credentials.flavor import BaseFlavor
from truvity_sdk.documents.helpers import generate_idempotency_key
from truvity_sdk.documents.types import CredentialBlob, CredentialDescriptor, CredentialMetadata, VerificationResult
from truvity_sdk.types.didcomm_message_send import DidcommMessageSend

class BaseVerifiableCredential:
    def __init__(
        self,
        client: TruvityApi,
        descriptor: CredentialDescriptor,
        blob: Optional[CredentialBlob],
        flavor: BaseFlavor = BaseFlavor(),
    ) -> None:
        self.client = client
        self.flavor = flavor
        self.descriptor = descriptor
        self.blob = blob

    def get_blob(self) -> CredentialBlob:
        if self.blob is None:
            response = self.client.credentials.credential_download(
                self.descriptor.id,
                self.descriptor.revision
            )

            self.blob = b''.join(response)

        return self.blob

    def get_meta_data(self) -> CredentialMetadata:
        return self.flavor.get_metadata(self.get_blob())

    def verify(self) -> VerificationResult:
        result = self.client.credentials.credential_verify(self.descriptor.id)

        return VerificationResult(verified=result.verified or False)

    def send(self, target_id: str, private_key_id: str) -> None:
        presentation_resource = self.client.presentations.presentation_issue(
            credentials_ids=[self.descriptor.id],
            key_id=private_key_id,
            #composition_type="EMBED",
        )

        self.client.didcomm_messages.didcomm_message_send(
            data=DidcommMessageSend(
                to=target_id,
                key_id=private_key_id,
                presentations=[presentation_resource.id],
            ),
            idempotency_key=generate_idempotency_key("send"),
        )

    def delete(self) -> None:
        self.client.credentials.credential_delete(self.descriptor.id,
            if_match=self.descriptor.etag,
            idempotency_key=generate_idempotency_key("delete"),
        )

class AsyncBaseVerifiableCredential:
    def __init__(
        self,
        client: AsyncTruvityApi,
        descriptor: CredentialDescriptor,
        blob: Optional[CredentialBlob],
        flavor: BaseFlavor = BaseFlavor(),
    ) -> None:
        self.client = client
        self.flavor = flavor
        self.descriptor = descriptor
        self.blob = blob

    async def get_blob(self) -> CredentialBlob:
        if self.blob is None:
            buffer = bytearray()

            async for chunk in self.client.credentials.credential_download(
                self.descriptor.id,
                self.descriptor.revision
            ):
                buffer.extend(chunk)

            self.blob = buffer

        return self.blob

    async def get_meta_data(self) -> CredentialMetadata:
        return self.flavor.get_metadata(await self.get_blob())

    async def verify(self) -> VerificationResult:
        result = await self.client.credentials.credential_verify(self.descriptor.id)

        return VerificationResult(verified=result.verified or False)

    async def send(self, target_id: str, private_key_id: str) -> None:
        presentation_resource = await self.client.presentations.presentation_issue(
            credentials_ids=[self.descriptor.id],
            key_id=private_key_id,
            #composition_type="EMBED",
        )

        await self.client.didcomm_messages.didcomm_message_send(
            data=DidcommMessageSend(
                to=target_id,
                key_id=private_key_id,
                presentations=[presentation_resource.id],
            ),
            idempotency_key=generate_idempotency_key("send"),
        )

    async def delete(self) -> None:
        await self.client.credentials.credential_delete(self.descriptor.id,
            if_match=self.descriptor.etag,
            idempotency_key=generate_idempotency_key("delete"),
        )
