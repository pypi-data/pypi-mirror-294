from typing import Optional, Type, TypeVar
from truvity_sdk.documents.credentials.base_verifiable_credential import AsyncBaseVerifiableCredential, BaseVerifiableCredential
from truvity_sdk.documents.credentials.issued import AsyncVerifiableCredential, VerifiableCredential
from truvity_sdk.documents.credentials.map import map_async, map_sync
from truvity_sdk.documents.document_model import DocumentModel

T = TypeVar("T", bound=DocumentModel)

class UnknownVerifiableCredential(BaseVerifiableCredential):
    def assert_is(self, model: Type[T]) -> Optional[VerifiableCredential[T]]:
        credential_resource = self.client.credentials.credential_revision(
            self.descriptor.id,
            self.descriptor.revision
        )
        if model.can_map(credential_resource):
            return map_sync(model, self.client, credential_resource)
        else:
            return None

class AsyncUnknownVerifiableCredential(AsyncBaseVerifiableCredential):
    async def assert_is(self, model: Type[T]) -> Optional[AsyncVerifiableCredential[T]]:
        credential_resource = await self.client.credentials.credential_revision(
            self.descriptor.id,
            self.descriptor.revision
        )

        if model.can_map(credential_resource):
            return map_async(model, self.client, credential_resource)
        else:
            return None
