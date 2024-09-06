from typing import Type, TypeVar, Union, overload

from truvity_sdk.client import AsyncTruvityApi, TruvityApi
from truvity_sdk.documents.credentials.draft import AsyncDraftCredential, DraftCredential
from truvity_sdk.documents.credentials.flavor import CredentialFlavor
from truvity_sdk.documents.credentials.issued import AsyncVerifiableCredential, VerifiableCredential
from truvity_sdk.documents.document_model import DocumentModel
from truvity_sdk.documents.types import CredentialDescriptor, DraftDataDescriptor
from truvity_sdk.types.credential_resource import CredentialResource
from truvity_sdk.types.draft_resource import DraftResource

T = TypeVar("T", bound=DocumentModel)

@overload
def map_sync(model: Type[T], client: TruvityApi, input: CredentialResource) -> VerifiableCredential[T]: ...
@overload
def map_sync(model: Type[T], client: TruvityApi, input: DraftResource) -> DraftCredential[T]: ...

def map_sync(model: Type[T], client: TruvityApi, input: Union[DraftResource, CredentialResource]) -> Union[VerifiableCredential[T], DraftCredential[T]]:
    if isinstance(input, CredentialResource):
        if not model.can_map(input):
            raise Exception(
                f"The received CredentialResource is incompatible with the current VcDecorator instance claims model: {model.vocab_name()}"
            )
        return VerifiableCredential(
            client,
            CredentialFlavor(model),
            CredentialDescriptor.from_resource(input),
            None,
        )
    elif isinstance(input, DraftResource):
        if not model.can_map(input):
            raise Exception(
                f"The received DraftResource is incompatible with the current VcDecorator instance claims model: {model.vocab_name()}"
            )
        return DraftCredential(
            client,
            CredentialFlavor(model),
            DraftDataDescriptor.from_resource(input),
            CredentialDescriptor.from_resource(input)
        )

@overload
def map_async(model: Type[T], client: AsyncTruvityApi, input: CredentialResource) -> AsyncVerifiableCredential[T]: ...
@overload
def map_async(model: Type[T], client: AsyncTruvityApi, input: DraftResource) -> AsyncDraftCredential[T]: ...

def map_async(model: Type[T], client: AsyncTruvityApi, input: Union[DraftResource, CredentialResource]) -> Union[AsyncVerifiableCredential[T], AsyncDraftCredential[T]]:
    if isinstance(input, CredentialResource):
        if not model.can_map(input):
            raise Exception(
                f"The received CredentialResource is incompatible with the current VcDecorator instance claims model: {model.vocab_name()}"
            )
        return AsyncVerifiableCredential(
            client,
            CredentialFlavor(model),
            CredentialDescriptor.from_resource(input),
            None,
        )
    elif isinstance(input, DraftResource):
        if not model.can_map(input):
            raise Exception(
                f"The received DraftResource is incompatible with the current VcDecorator instance claims model: {model.vocab_name()}"
            )
        return AsyncDraftCredential(
            client,
            CredentialFlavor(model),
            DraftDataDescriptor.from_resource(input),
            CredentialDescriptor.from_resource(input)
        )
