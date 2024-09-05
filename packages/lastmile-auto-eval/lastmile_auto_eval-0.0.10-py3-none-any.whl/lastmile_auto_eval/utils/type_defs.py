"""
Helper file for defining types and classes
"""

from dataclasses import dataclass
import datetime
from enum import Enum
from typing import Any, NewType, Optional
import json

EvaluationResult = NewType("EvaluationResult", dict[str, list[float]])


class JobStatus(str, Enum):
    """
    The status of a job.
    """

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Visibility(str, Enum):
    """
    The visibility of a job.
    """

    # Only creator can see it
    PRIVATE = "private"

    # Creator and other members within an org can see it
    MEMBER = "member"

    # Anyone can see it
    PUBLIC = "public"


@dataclass(frozen=True)
class JobInfo:
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    status: JobStatus
    visibility: Visibility

    def __repr__(self) -> str:
        return json.dumps(
            {
                "id": self.id,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat(),
                "status": self.status.name,
                "visibility": self.visibility.name,
            },
            indent=2,
        )


@dataclass(frozen=True)
class JobEntry:
    """
    Represents a single entry in an evaluation request.
    Ie. if a request was sent with 1000 rows of data, there should be 1000 entries.
    """

    id: str
    request_index: int
    data: dict[str, str]

    def __repr__(self) -> str:
        return json.dumps(
            self.__dict__,
            indent=2,
        )


@dataclass(frozen=True)
class JobMetric:
    """
    Used to represent a metric that is returned alongside of a JobEntryScore.
    This is different from EvaluationMetric. EvaluationMetric is used to specify
    which metrics should be used in an evaluation request. JobMetric
    returns the name and id that a metric is associated with when evaluating
    a JobEntry. This is important because the name of a metric may change
    over time but it's id does not.
    """

    id: str
    name: str

    def __repr__(self) -> str:
        return json.dumps(
            {
                "id": self.id,
                "name": self.name,
            },
            indent=2,
        )


@dataclass(frozen=True)
class JobResultStatus:
    """
    Represents the result status of a JobEntryScore.
    """

    code: int
    message: str
    details: Optional[Any] = None

    def __repr__(self) -> str:
        return json.dumps(
            self.to_dict(),
            indent=2,
        )

    def to_dict(self) -> dict[str, str | int]:
        disp = {
            "code": self.code,
            "message": self.message,
        }
        if self.details is not None:
            disp["details"] = self.details.__repr__()
        return disp


@dataclass(frozen=True)
class JobEntryScore:
    metric: JobMetric
    score: Optional[float]
    # If the score is not available, provide details about the request
    status: Optional[JobResultStatus] = None

    def __repr__(self) -> str:
        return json.dumps(
            self.to_dict(),
            indent=2,
        )

    def to_dict(self) -> dict[str, Any]:
        disp = {
            "metric": self.metric.__dict__,
            "score": self.score,
        }
        if isinstance(self.status, JobResultStatus):
            disp["status"] = self.status.to_dict()
        return disp


@dataclass(frozen=True)
class JobEntryResult:
    """
    Represents a set of evaluation scores for a single entry.
    There is one score per metric. Ie: if a request was sent
    with 3 metrics, each entry will contain 3 scores.
    """

    entry: JobEntry
    scores: list[JobEntryScore]

    def __repr__(self) -> str:
        return json.dumps(
            self.to_dict(),
            indent=2,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry": self.entry.__dict__,
            "scores": list(map(lambda s: s.to_dict(), self.scores)),
        }


class EvaluationMetric(str, Enum):
    """
    Used to specify which metric to evaluate with during an evaluation request.
    """

    P_FAITHFUL = "p_faithful"
    RELEVANCE = "relevance"
    TOXICITY = "toxicity"
    QA = "qa"
    SUMMARIZATION = "summarization"


@dataclass(frozen=True)
class ModelSpecifier:
    """
    Used to specify more fine-grained control over which version of metrics to evaluate with.
    """

    identifier: EvaluationMetric | str
    version: str = "latest"


class StreamConfig(str, Enum):
    """
    Internal intermediate flag to make it easier to know
    which streaming-type request we should make.
    """

    NO_STREAMING = "no_streaming"
    REQUEST_STREAMING_ONLY = "request_streaming_only"
    RESPONSE_STREAMING_ONLY = "response_streaming_only"
    BIDIRECTIONAL_STREAMING = "bidirectional_streaming"
