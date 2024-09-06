from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from typing_extensions import Self

from truvity_sdk.types.credential_resource import CredentialResource
from truvity_sdk.types.draft_resource import DraftResource
from truvity_sdk.types.presentation_resource import PresentationResource

CredentialBlob = bytes

Claims = Dict[str, Any]

@dataclass
class CredentialDescriptor:
    id: str
    etag: str
    revision: int

    @classmethod
    def from_resource(cls, resource: Union[CredentialResource, DraftResource]) -> Self:
        return cls(
            id=resource.id,
            etag=resource.etag,
            revision=resource.revision,
        )

@dataclass
class PresentationDescriptor:
    id: str
    etag: str
    revision: int
    data_linked_credentials: List[str]

    @classmethod
    def from_presentation_resource(cls, resource: PresentationResource) -> Self:
        return cls(
            id=resource.id,
            etag=resource.etag,
            revision=resource.revision,
            data_linked_credentials=resource.data.linked_credentials
        )


@dataclass
class DraftMetadata:
    subject: Optional[str]
    expiration_date: Optional[datetime]

@dataclass
class CredentialMetadata:
    subject: Optional[str]
    expiration_date: Optional[datetime]
    id: str
    issuer: str
    issuance_date: datetime

@dataclass
class VerificationResult:
    verified: bool

@dataclass
class DraftDataDescriptor:
    subject: Optional[str]
    valid_until: Optional[datetime]
    values: Optional[Claims]

    @classmethod
    def from_resource(cls, input: DraftResource) -> Self:
        return cls(
            subject=input.data.meta.subject if input.data.meta is not None else None,
            valid_until=input.data.meta.valid_until if input.data.meta is not None else None,
            values=input.data.values
        )

@dataclass
class UpdatePayload:
    annotations: Optional[Dict[str, str]]
    labels: Optional[Dict[str, str]]
