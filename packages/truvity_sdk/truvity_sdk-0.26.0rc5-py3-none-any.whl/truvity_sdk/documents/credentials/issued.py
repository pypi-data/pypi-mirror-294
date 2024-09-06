from typing import Generic, Optional, TypeVar, cast
from truvity_sdk.client import AsyncTruvityApi, TruvityApi
from truvity_sdk.documents.credentials.base_verifiable_credential import AsyncBaseVerifiableCredential, BaseVerifiableCredential
from truvity_sdk.documents.credentials.flavor import CredentialFlavor
from truvity_sdk.documents.document_model import DocumentModel
from truvity_sdk.documents.types import CredentialBlob, CredentialDescriptor

T = TypeVar("T", bound=DocumentModel)

class VerifiableCredential(Generic[T], BaseVerifiableCredential):
    def __init__(
        self,
        client: TruvityApi,
        flavor: CredentialFlavor[T],
        descriptor: CredentialDescriptor,
        blob: Optional[CredentialBlob]
    ) -> None:
        super().__init__(client, descriptor, blob, flavor)

    def get_claims(self) -> T:
        flavor = cast(CredentialFlavor, self.flavor)
        return flavor.model.from_api_values(
            flavor.get_claims(self.get_blob())
        )

class AsyncVerifiableCredential(Generic[T], AsyncBaseVerifiableCredential):
    def __init__(
        self,
        client: AsyncTruvityApi,
        flavor: CredentialFlavor[T],
        descriptor: CredentialDescriptor,
        blob: Optional[CredentialBlob]
    ) -> None:
        super().__init__(client, descriptor, blob, flavor)

    async def get_claims(self) -> T:
        flavor = cast(CredentialFlavor, self.flavor)
        return flavor.model.from_api_values(
            flavor.get_claims(await self.get_blob())
        )
