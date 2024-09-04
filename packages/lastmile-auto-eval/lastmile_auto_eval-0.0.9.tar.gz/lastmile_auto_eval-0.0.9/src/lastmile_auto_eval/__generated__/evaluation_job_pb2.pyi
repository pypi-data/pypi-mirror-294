import status_pb2 as _status_pb2
import common_pb2 as _common_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class JobStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    QUEUED: _ClassVar[JobStatus]
    RUNNING: _ClassVar[JobStatus]
    COMPLETED: _ClassVar[JobStatus]
    CANCELLED: _ClassVar[JobStatus]
QUEUED: JobStatus
RUNNING: JobStatus
COMPLETED: JobStatus
CANCELLED: JobStatus

class JobId(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class JobIds(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedCompositeFieldContainer[JobId]
    def __init__(self, ids: _Optional[_Iterable[_Union[JobId, _Mapping]]] = ...) -> None: ...

class GetJobParams(_message.Message):
    __slots__ = ("ids", "orgId")
    IDS_FIELD_NUMBER: _ClassVar[int]
    ORGID_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    orgId: str
    def __init__(self, ids: _Optional[_Iterable[str]] = ..., orgId: _Optional[str] = ...) -> None: ...

class JobInfo(_message.Message):
    __slots__ = ("id", "createdAt", "updatedAt", "creator", "organization", "status", "visibility")
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATEDAT_FIELD_NUMBER: _ClassVar[int]
    UPDATEDAT_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    id: str
    createdAt: _timestamp_pb2.Timestamp
    updatedAt: _timestamp_pb2.Timestamp
    creator: _common_pb2.Creator
    organization: _common_pb2.Organization
    status: JobStatus
    visibility: _common_pb2.Visibility
    def __init__(self, id: _Optional[str] = ..., createdAt: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updatedAt: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., creator: _Optional[_Union[_common_pb2.Creator, _Mapping]] = ..., organization: _Optional[_Union[_common_pb2.Organization, _Mapping]] = ..., status: _Optional[_Union[JobStatus, str]] = ..., visibility: _Optional[_Union[_common_pb2.Visibility, str]] = ...) -> None: ...

class JobResults(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[JobResult]
    def __init__(self, results: _Optional[_Iterable[_Union[JobResult, _Mapping]]] = ...) -> None: ...

class JobResult(_message.Message):
    __slots__ = ("entry", "scores")
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    entry: DataEntry
    scores: _containers.RepeatedCompositeFieldContainer[Score]
    def __init__(self, entry: _Optional[_Union[DataEntry, _Mapping]] = ..., scores: _Optional[_Iterable[_Union[Score, _Mapping]]] = ...) -> None: ...

class DataEntry(_message.Message):
    __slots__ = ("id", "requestIndex", "data")
    ID_FIELD_NUMBER: _ClassVar[int]
    REQUESTINDEX_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    requestIndex: int
    data: _any_pb2.Any
    def __init__(self, id: _Optional[str] = ..., requestIndex: _Optional[int] = ..., data: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...

class Score(_message.Message):
    __slots__ = ("metric", "score", "status")
    METRIC_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    metric: Metric
    score: float
    status: _status_pb2.Status
    def __init__(self, metric: _Optional[_Union[Metric, _Mapping]] = ..., score: _Optional[float] = ..., status: _Optional[_Union[_status_pb2.Status, _Mapping]] = ...) -> None: ...

class Metric(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class UpdateJobParams(_message.Message):
    __slots__ = ("id", "status", "visibility")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: JobStatus
    visibility: _common_pb2.Visibility
    def __init__(self, id: _Optional[str] = ..., status: _Optional[_Union[JobStatus, str]] = ..., visibility: _Optional[_Union[_common_pb2.Visibility, str]] = ...) -> None: ...

class DeleteJobResponse(_message.Message):
    __slots__ = ("id", "status")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: _status_pb2.Status
    def __init__(self, id: _Optional[str] = ..., status: _Optional[_Union[_status_pb2.Status, _Mapping]] = ...) -> None: ...
