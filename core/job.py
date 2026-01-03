from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from uuid import uuid4

class JobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class Job:
    id: str = field(default_factory=lambda: str(uuid4()))
    type: str = ""
    status: JobStatus = JobStatus.PENDING
    payload: Any = None
    retry_count: int = 0
    max_retries: int = 3

    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    error_message: Optional[str] = None
