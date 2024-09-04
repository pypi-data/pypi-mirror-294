"""
Helper file for defining types and classes
"""

from dataclasses import dataclass
import datetime
from enum import Enum
from typing import NewType
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


class EvaluationMetric(str, Enum):
    P_FAITHFUL = "p_faithful"
    RELEVANCE = "relevance"
    TOXICITY = "toxicity"
    QA = "qa"
    SUMMARIZATION = "summarization"


@dataclass(frozen=True)
class ModelSpecifier:
    """
    Use this to specify more fine-grained control over which models to evaluate.
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
