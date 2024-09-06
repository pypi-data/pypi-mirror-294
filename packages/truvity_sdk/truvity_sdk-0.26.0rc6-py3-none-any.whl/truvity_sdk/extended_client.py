
from typing import Type, TypeVar
from truvity_sdk.client import AsyncTruvityApi, TruvityApi
from truvity_sdk.documents.credential import AsyncVcDecorator, VcDecorator
from truvity_sdk.documents.document_model import DocumentModel
from truvity_sdk.documents.presentation import AsyncVpDecorator, VpDecorator

T = TypeVar("T", bound=DocumentModel)

class TruvityApiExtendedClient(TruvityApi):
    def vc_decorator(self, model: Type[T]) -> VcDecorator[T]:
        return VcDecorator(self, model)

    def vp_decorator(self) -> VpDecorator:
        return VpDecorator(self)

class AsyncTruvityApiExtendedClient(AsyncTruvityApi):
    def vc_decorator(self, model: Type[T]) -> AsyncVcDecorator[T]:
        return AsyncVcDecorator(self, model)

    def vp_decorator(self) -> AsyncVpDecorator:
        return AsyncVpDecorator(self)
