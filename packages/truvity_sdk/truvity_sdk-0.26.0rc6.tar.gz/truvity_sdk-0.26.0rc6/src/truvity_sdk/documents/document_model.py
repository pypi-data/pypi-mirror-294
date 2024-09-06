from dataclasses import dataclass
from datetime import date, datetime
import dateutil.parser
from typing_extensions import dataclass_transform, Self
from typing import Any, Dict, Generic, List, Literal, Optional, Tuple, Type, TypeVar, Union
import typing

from truvity_sdk.documents.types import Claims
from truvity_sdk.types.credential_resource import CredentialResource
from truvity_sdk.types.draft_enum_value import DraftEnumValue
from truvity_sdk.types.draft_resource import DraftResource
from truvity_sdk.types.draft_schema_fields_item import DraftSchemaFieldsItem, DraftSchemaFieldsItem_Boolean, DraftSchemaFieldsItem_Date, DraftSchemaFieldsItem_Datetime, DraftSchemaFieldsItem_File, DraftSchemaFieldsItem_Link, DraftSchemaFieldsItem_Number, DraftSchemaFieldsItem_String, DraftSchemaFieldsItem_Struct
from truvity_sdk.types.draft_show_schema import DraftShowSchema

# There's no simple way to define a type for all types and type annotations
# So we define this alias here to make it clear what we mean
FieldType = Any

class UnsupportedDataTypeInDocumentModel(Exception):
    def __init__(self, typ: FieldType) -> None:
        super().__init__(f"Unsupported data type in DocumentModel: '{typ.__name__}'")

@dataclass
class FieldOptions:
    title: Optional[str]
    enum_titles: Optional[Dict[str, str]]

def field(*, title: Optional[str] = None, enum_titles: Optional[Dict[str, str]] = None) -> Any:
    return FieldOptions(
        title=title,
        enum_titles=enum_titles
    )

def unwrap_optional_type(t: FieldType) -> Tuple[type, bool]:
    if typing.get_origin(t) == Union and len(typing.get_args(t)) == 2:
        union_args = typing.get_args(t)
        if union_args[0] == None.__class__:
            return union_args[1], False
        elif union_args[1] == None.__class__:
            return union_args[0], False
    elif typing.get_origin(t) == Optional:
        return typing.get_args(t)[0], False
    return t, True

def unwrap_list_type(t: FieldType) -> Tuple[type, bool]:
    if typing.get_origin(t) == list:
        return typing.get_args(t)[0], True
    return t, False

def extract_enum_string_values(field_type: FieldType, titles=Optional[Dict[str, str]]) -> Tuple[FieldType, Optional[List[DraftEnumValue]]]:
    enum_values = None
    stack = [field_type]
    while len(stack) > 0:
        t = stack.pop()
        if typing.get_origin(t) == Union or typing.get_origin(t) == Literal:
            for arg in typing.get_args(t):
                if isinstance(arg, str):
                    enum_values = enum_values or []
                    enum_values_args = {'value': arg}
                    if titles is not None and arg in titles:
                        enum_values_args['title'] = titles[arg]
                    enum_values.append(DraftEnumValue(**enum_values_args))
                elif typing.get_origin(arg) == Literal:
                    stack.append(arg)
                else:
                    return field_type, None
    if enum_values is None:
        return field_type, None
    else:
        return str, enum_values

@dataclass
class FieldDescription:
    name: str
    base_type: FieldType
    is_array: bool
    not_empty: bool
    title: Optional[str]
    enum_values: Optional[List[DraftEnumValue]]
    original_type: FieldType

    def __init__(self, field_name: str, field_type: FieldType, options: FieldOptions) -> None:
        self.name = field_name
        self.original_type = field_type
        self.title = options.title

        value_field_type, not_empty = unwrap_optional_type(field_type)
        value_field_type, is_array = unwrap_list_type(value_field_type)
        value_field_type, enum_values = extract_enum_string_values(value_field_type, options.enum_titles)

        self.base_type = value_field_type
        self.is_array = is_array
        self.not_empty = not_empty
        self.enum_values = enum_values

    def to_draft_schema_field_item(self) -> DraftSchemaFieldsItem:
        args: Dict[str, Any] = {
            'name': self.name,
        }
        if self.is_array:
            args['is_array'] = True
        if self.title is not None:
            args['title'] = self.title
        if self.not_empty:
            args['not_empty'] = True

        if self.base_type == str:
            if self.enum_values is not None:
                args['enum'] = self.enum_values
            return DraftSchemaFieldsItem_String(
                kind='STRING',
                **args,
            )
        elif self.base_type == int or self.base_type == float:
            return DraftSchemaFieldsItem_Number(
                kind='NUMBER',
                **args
            )
        elif self.base_type == bool:
            return DraftSchemaFieldsItem_Boolean(
                kind='BOOLEAN',
                **args
            )
        elif self.base_type == datetime:
            return DraftSchemaFieldsItem_Datetime(
                kind='DATETIME',
                **args
            )
        elif self.base_type == date:
            return DraftSchemaFieldsItem_Date(
                kind='DATE',
                **args
            )
        elif self.base_type == LinkedFile:
            return DraftSchemaFieldsItem_File(
                kind='FILE',
                **args
            )
        elif typing.get_origin(self.base_type) == LinkedCredential:
            return DraftSchemaFieldsItem_Link(
                kind='LINK',
                **args
            )
        elif issubclass(self.base_type, DocumentModel):
            field_draft_schema: DraftShowSchema = getattr(self.base_type, '__draft_schema')
            return DraftSchemaFieldsItem_Struct(
                vocab_name=field_draft_schema.vocab_name,
                vocab_namespace=field_draft_schema.vocab_namespace,
                kind="STRUCT",
                fields=field_draft_schema.fields,
                **args
            )
        else:
            raise UnsupportedDataTypeInDocumentModel(self.original_type)

@dataclass_transform(field_specifiers=(FieldOptions, field), kw_only_default=True)
class DocumentModel:
    def __init_subclass__(cls: type, *, namespace: str, name: Optional[str] = None, vc_type: Optional[List[str]] = None) -> None:
        if name is None:
            name = cls.__name__

        field_descriptions = [
            FieldDescription(field_name, field_type, getattr(cls, field_name, field()))
            for field_name, field_type
            in cls.__annotations__.items()
        ]

        setattr(cls, '__vocab_namespace', namespace)
        setattr(cls, '__vocab_name', name)
        setattr(cls, '__vc_type', vc_type)
        setattr(cls, '__field_descriptions', field_descriptions)


        draft_schema_extra_args = {}
        if vc_type is not None:
            draft_schema_extra_args['vc_type'] = vc_type

        setattr(cls, '__draft_schema', DraftShowSchema(
            fields=[field.to_draft_schema_field_item() for field in field_descriptions],
            vocab_namespace=namespace,
            vocab_name=name,
            **draft_schema_extra_args
        ))

    def __init__(self, **kwargs):
        for field in self.field_descriptions():
            if field.name in kwargs:
                setattr(self, field.name, kwargs[field.name])
            else:
                setattr(self, field, None)

    def __repr__(self):
        field_str = ", ".join(f"{field.name}={repr(getattr(self, field.name))}" for field in self.field_descriptions())
        return f"{self.__class__.__name__}({field_str})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return all(getattr(self, field.name) == getattr(other, field.name) for field in self.field_descriptions())

    def to_api_values(self) -> Claims:
        def __udt_value_to_api_value(value: Any, typ: FieldType) -> Any:
            if typ == str or typ == int or typ == float or typ == float or typ == bool:
                return value
            elif typ == date:
                return value.isoformat()
            elif typ == datetime:
                return value.isoformat()
            elif typing.get_origin(typ) == LinkedCredential:
                return {"id": f"urn:credential:{value.id}", "type": "LinkedCredential"}
            elif typ == LinkedFile:
                return {"id": f"urn:file:{value.id}", "type": "LinkedFile"}
            elif issubclass(typ, DocumentModel):
                return value.to_api_values()
            else:
                raise UnsupportedDataTypeInDocumentModel(typ)

        values: Claims = {}
        for field in self.field_descriptions():
            value = getattr(self, field.name)
            if value is None:
                if field.not_empty:
                    raise Exception(f"Unexpected None in field ({field.name}) with not_empty=True")
                values[field.name] = None
            elif field.is_array:
                values[field.name] = [__udt_value_to_api_value(x, field.base_type) for x in value]
            else:
                values[field.name] = __udt_value_to_api_value(value, field.base_type)
        return values

    @classmethod
    def iri(cls) -> str:
        return f"{cls.vocab_namespace()}#${cls.vocab_name()}"

    @classmethod
    def credential_term(cls) -> str:
        return f"{cls.vocab_name()}Credential"

    @classmethod
    def can_map(cls, input: Union[DraftResource, CredentialResource]) -> bool:
        return cls.credential_term() in input.data.type

    @classmethod
    def from_api_values(cls, input: Claims) -> Self:
        def __api_value_to_model_value(
            value: Any,
            typ: FieldType
        ) -> Any:
            if typ == str or typ == int or typ == float or typ == bool:
                return value
            elif typ == date:
                return date.fromisoformat(value)
            elif typ == datetime:
                return dateutil.parser.isoparse(value)
            elif typing.get_origin(typ) == LinkedCredential:
                return LinkedCredential(model=typing.get_args(typ)[0], id=value["id"].split(":")[2])
            elif typ == LinkedFile:
                return LinkedFile(id=value["id"].split(":")[2])
            elif issubclass(typ, DocumentModel):
                return typ.from_api_values(value)
            else:
                raise UnsupportedDataTypeInDocumentModel(typ)

        kwargs: Dict[str, Any] = {}
        for field in cls.field_descriptions():
            value = input.get(field.name)
            if value is None:
                if field.not_empty:
                    raise Exception(f"Invalid api value for field {cls.vocab_name()}.{field.name}: Unexpected None")
                kwargs[field.name] = None
            elif field.is_array:
                if not isinstance(value, list):
                    raise Exception(f"Invalid api value for field {cls.vocab_name()}.{field.name}: Expected list")
                kwargs[field.name] = [__api_value_to_model_value(x, field.base_type) for x in value]
            else:
                kwargs[field.name] = __api_value_to_model_value(value, field.base_type)
        return cls(**kwargs)

    @classmethod
    def field_descriptions(cls: type) -> List[FieldDescription]:
        return getattr(cls, '__field_descriptions')

    @classmethod
    def vocab_namespace(cls: type) -> str:
        return getattr(cls, '__vocab_namespace')

    @classmethod
    def vocab_name(cls: type) -> str:
        return getattr(cls, '__vocab_name')

    @classmethod
    def vc_type(cls: type) -> str:
        return getattr(cls, '__vc_type')

    @classmethod
    def draft_schema(cls: type) -> DraftShowSchema:
        return getattr(cls, '__draft_schema')

T = TypeVar("T", bound=DocumentModel)

@dataclass
class LinkedFile:
    id: str

@dataclass
class LinkedCredential(Generic[T]):
    id: str
    model: Type[T]
