from dataclasses import dataclass
from typing import Dict, Generic, Optional, TypeVar, cast
from typing_extensions import Self

from truvity_sdk.client import AsyncTruvityApi, TruvityApi
from truvity_sdk.documents.credentials.flavor import CredentialFlavor
from truvity_sdk.documents.credentials.issued import AsyncVerifiableCredential, VerifiableCredential
from truvity_sdk.documents.document_model import DocumentModel
from truvity_sdk.documents.helpers import generate_idempotency_key
from truvity_sdk.documents.types import CredentialDescriptor, DraftDataDescriptor, DraftMetadata
from truvity_sdk.types.draft import Draft
from truvity_sdk.types.draft_meta import DraftMeta

T = TypeVar("T", bound=DocumentModel)

@dataclass
class UpdatePayloadWithClaims(Generic[T]):
    claims: Optional[T]
    metadata: Optional[DraftMetadata]
    annotations: Optional[Dict[str, str]]
    labels: Optional[Dict[str, str]]

class DraftCredential(Generic[T]):
    def __init__(
        self,
        client: TruvityApi,
        flavor: CredentialFlavor,
        draft_data: DraftDataDescriptor,
        descriptor: CredentialDescriptor
    ) -> None:
        self.client = client
        self.flavor = flavor
        self.draft_data = draft_data
        self.descriptor = descriptor

    def claims(self) -> Optional[T]:
        if self.draft_data is None or self.draft_data.values is None:
            return None
        return self.flavor.model(self.draft_data.values)

    def metadata(self) -> Optional[DraftMetadata]:
        return DraftMetadata(
            subject=self.draft_data.subject,
            expiration_date=self.draft_data.valid_until
        ) if self.draft_data is not None else None

    def update(self, request: UpdatePayloadWithClaims[T]) -> Self:
        updated = self.client.drafts.draft_update(self.descriptor.id,
            if_match=self.descriptor.etag,
            idempotency_key=generate_idempotency_key("update"),
            data=Draft(
                values=request.claims.to_api_values()
                if request.claims is not None else None,
                meta=DraftMeta(
                    subject=request.metadata.subject,
                    valid_until=request.metadata.expiration_date
                ) if request.metadata is not None else None,
            ),
            annotations=request.annotations,
            labels=request.labels,
        )

        return cast(Self, DraftCredential(
            self.client,
            self.flavor,
            DraftDataDescriptor.from_resource(updated),
            CredentialDescriptor.from_resource(updated)
        ))

    def delete(self) -> None:
        self.client.drafts.draft_delete(self.descriptor.id,
            if_match=self.descriptor.etag,
            idempotency_key=generate_idempotency_key("delete"),
        )

    def issue(self, private_key_id: str) -> VerifiableCredential[T]:
        issued = self.client.drafts.draft_issue(
            self.descriptor.id,
            self.descriptor.revision,
            key_id=private_key_id,
        )

        return VerifiableCredential(
            self.client,
            self.flavor,
            CredentialDescriptor.from_resource(issued),
            None
        )

class AsyncDraftCredential(Generic[T]):
    def __init__(
        self,
        client: AsyncTruvityApi,
        flavor: CredentialFlavor,
        draft_data: DraftDataDescriptor,
        descriptor: CredentialDescriptor
    ) -> None:
        self.client = client
        self.flavor = flavor
        self.draft_data = draft_data
        self.descriptor = descriptor

    def claims(self) -> Optional[T]:
        if self.draft_data is None or self.draft_data.values is None:
            return None
        return self.flavor.model.from_api_values(self.draft_data.values)

    def metadata(self) -> Optional[DraftMetadata]:
        return DraftMetadata(
            subject=self.draft_data.subject,
            expiration_date=self.draft_data.valid_until
        ) if self.draft_data is not None else None

    async def update(self, request: UpdatePayloadWithClaims[T]) -> Self:
        updated = await self.client.drafts.draft_update(self.descriptor.id,
            if_match=self.descriptor.etag,
            idempotency_key=generate_idempotency_key("update"),
            data=Draft(
                values= request.claims.to_api_values()
                    if request.claims is not None else None,
                meta=DraftMeta(
                    subject=request.metadata.subject,
                    valid_until=request.metadata.expiration_date
                ) if request.metadata is not None else None,
            ),
            annotations=request.annotations,
            labels=request.labels,
        )

        return cast(Self, AsyncDraftCredential(
            self.client,
            self.flavor,
            DraftDataDescriptor.from_resource(updated),
            CredentialDescriptor.from_resource(updated)
        ))

    async def delete(self) -> None:
        await self.client.drafts.draft_delete(self.descriptor.id,
            if_match=self.descriptor.etag,
            idempotency_key=generate_idempotency_key("delete"),
        )

    async def issue(self, private_key_id: str) -> AsyncVerifiableCredential[T]:
        issued = await self.client.drafts.draft_issue(
            self.descriptor.id,
            self.descriptor.revision,
            key_id=private_key_id,
        )

        return AsyncVerifiableCredential(
            self.client,
            self.flavor,
            CredentialDescriptor.from_resource(issued),
            None
        )
