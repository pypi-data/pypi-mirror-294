import asyncio
from typing import List
from truvity_sdk.client import AsyncTruvityApi, TruvityApi
from truvity_sdk.documents.credentials.unknown import AsyncUnknownVerifiableCredential, UnknownVerifiableCredential
from truvity_sdk.documents.helpers import generate_idempotency_key
from truvity_sdk.documents.types import CredentialDescriptor, PresentationDescriptor, VerificationResult
from truvity_sdk.types.didcomm_message_send import DidcommMessageSend

class VerifiablePresentation:
    def __init__(self, client: TruvityApi, descriptor: PresentationDescriptor) -> None:
        self.client = client
        self.descriptor = descriptor

    def get_credentials(self) -> List[UnknownVerifiableCredential]:
        return [
            UnknownVerifiableCredential(
                self.client,
                descriptor=CredentialDescriptor.from_resource(
                    self.client.credentials.credential_latest(id.split(":")[2])
                ),
                blob=None
            ) for id in self.descriptor.data_linked_credentials
        ]

    def verify(self) -> VerificationResult:
        result = self.client.presentations.presentation_verify(self.descriptor.id)

        return VerificationResult(result.verified or False)

    def send(self, target_id: str, private_key_id: str) -> None:
        self.client.didcomm_messages.didcomm_message_send(
            data=DidcommMessageSend(
                to=target_id,
                key_id=private_key_id,
                presentations=[self.descriptor.id],
            ),
            idempotency_key=generate_idempotency_key("send"),
        )

class AsyncVerifiablePresentation:
    def __init__(self, client: AsyncTruvityApi, descriptor: PresentationDescriptor) -> None:
        self.client = client
        self.descriptor = descriptor

    async def get_credentials(self) -> List[AsyncUnknownVerifiableCredential]:
        credential_resources = await asyncio.gather(*[
            self.client.credentials.credential_latest(id.split(":")[2])
            for id in self.descriptor.data_linked_credentials
        ])
        return [
            AsyncUnknownVerifiableCredential(
                self.client,
                descriptor=CredentialDescriptor.from_resource(x),
                blob=None
            ) for x in credential_resources
        ]

    async def verify(self) -> VerificationResult:
        result = await self.client.presentations.presentation_verify(self.descriptor.id)

        return VerificationResult(result.verified or False)

    async def send(self, target_id: str, private_key_id: str) -> None:
        await self.client.didcomm_messages.didcomm_message_send(
            data=DidcommMessageSend(
                to=target_id,
                key_id=private_key_id,
                presentations=[self.descriptor.id],
            ),
            idempotency_key=generate_idempotency_key("send"),
        )

def issue(
    client: TruvityApi,
    credential_ids: List[str],
    private_key_id: str
) -> VerifiablePresentation:

    presentation_resource = client.presentations.presentation_issue(
        credentials_ids=credential_ids,
        key_id=private_key_id,
        #composition_type="EMBED",
    )

    return VerifiablePresentation(
        client,
        PresentationDescriptor.from_presentation_resource(presentation_resource)
    )

async def issue_async(
    client: AsyncTruvityApi,
    credential_ids: List[str],
    private_key_id: str
) -> AsyncVerifiablePresentation:

    presentation_resource = await client.presentations.presentation_issue(
        credentials_ids=credential_ids,
        key_id=private_key_id,
        #composition_type="EMBED",
    )

    return AsyncVerifiablePresentation(
        client,
        PresentationDescriptor.from_presentation_resource(presentation_resource)
    )
