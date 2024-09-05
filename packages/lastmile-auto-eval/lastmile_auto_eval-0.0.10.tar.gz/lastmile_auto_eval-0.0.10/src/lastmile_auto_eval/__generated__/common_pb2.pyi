from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Visibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PRIVATE: _ClassVar[Visibility]
    MEMBER: _ClassVar[Visibility]
    PUBLIC: _ClassVar[Visibility]
PRIVATE: Visibility
MEMBER: Visibility
PUBLIC: Visibility

class Creator(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Organization(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class StringList(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class ModelSpecifier(_message.Message):
    __slots__ = ("identifier", "version")
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    identifier: str
    version: str
    def __init__(self, identifier: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class RequestBody(_message.Message):
    __slots__ = ("input", "ground_truth", "context", "output", "model_specifiers")
    INPUT_FIELD_NUMBER: _ClassVar[int]
    GROUND_TRUTH_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    MODEL_SPECIFIERS_FIELD_NUMBER: _ClassVar[int]
    input: StringList
    ground_truth: StringList
    context: StringList
    output: StringList
    model_specifiers: _containers.RepeatedCompositeFieldContainer[ModelSpecifier]
    def __init__(self, input: _Optional[_Union[StringList, _Mapping]] = ..., ground_truth: _Optional[_Union[StringList, _Mapping]] = ..., context: _Optional[_Union[StringList, _Mapping]] = ..., output: _Optional[_Union[StringList, _Mapping]] = ..., model_specifiers: _Optional[_Iterable[_Union[ModelSpecifier, _Mapping]]] = ...) -> None: ...
