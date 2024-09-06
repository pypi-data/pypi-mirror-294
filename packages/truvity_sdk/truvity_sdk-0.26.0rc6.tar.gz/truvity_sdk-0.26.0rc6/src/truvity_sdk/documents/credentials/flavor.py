import json
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, TypedDict, Union, cast
import urllib

import dateutil.parser

from truvity_sdk.documents.document_model import DocumentModel
from truvity_sdk.documents.types import CredentialBlob, CredentialMetadata

VcJsonLdSchema = TypedDict('VcJsonLdSchema', {
    '@context': Union[str, dict],
    'id': str,
    'type': List[str],
    'holder': Optional[str],
    'issuer': str,
    'issuanceDate': str,
    'expirationDate': Optional[str],
    'credentialSubject': dict,
    'proof': dict,
})

T = TypeVar("T", bound=DocumentModel)

class BaseFlavor:
    def _blob_to_json(self, input: CredentialBlob) -> VcJsonLdSchema:
        return json.loads(input.decode("utf-8"))

    def get_metadata(self, blob: CredentialBlob) -> CredentialMetadata:
        credential = self._blob_to_json(blob)

        if credential.get('id') is None:
            raise Exception("Issued credential is missing the 'id' information")
        if credential.get('issuer') is None:
            raise Exception("Issued credential is missing the 'issuer' information")
        if credential.get('issuanceDate') is None:
            raise Exception("Issued credential is missing the 'issuanceDate' information")

        return CredentialMetadata(
            id=cast(str, credential['id']),
            issuer=cast(str, credential['issuer']),
            issuance_date=dateutil.parser.isoparse(cast(str,credential['issuanceDate'])),
            subject=credential['credentialSubject'].get('id'),
            expiration_date=dateutil.parser.isoparse(cast(str, credential['expirationDate'])) if credential.get('expirationDate') is not None else None
        )

class CredentialFlavor(Generic[T], BaseFlavor):
    def __init__(self, model: Type[T]) -> None:
        self.model = model

    def __escape_term_name(self, name: str) -> str:
        # The term's names in JSON-LD have constraints on allowed characters.
        return urllib.parse.quote(name, safe='~()*!\'')

    def get_claims(self, blob: CredentialBlob) -> Dict[str, Any]:
        credential = self._blob_to_json(blob)

        credentialSubject = credential['credentialSubject']
        credentialSubject.pop("id", None)
        credentialSubject.pop("type", None)

        # TODO: implement proper input validation
        return credentialSubject

    def get_claims_type(self) -> str:
        return self.__escape_term_name(self.model.vocab_name())
