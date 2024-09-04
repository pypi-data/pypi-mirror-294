import lastmile_auto_eval.__generated__.common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class FloatList(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, values: _Optional[_Iterable[float]] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("scores",)

    class ScoresEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: FloatList
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[FloatList, _Mapping]] = ...,
        ) -> None: ...

    SCORES_FIELD_NUMBER: _ClassVar[int]
    scores: _containers.MessageMap[str, FloatList]
    def __init__(
        self, scores: _Optional[_Mapping[str, FloatList]] = ...
    ) -> None: ...
