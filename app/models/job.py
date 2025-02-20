from pydantic import BaseModel
from enum import Enum


class JobStatus (str, Enum):
    SUBMITTED = "submitted"     # Job has been submitted to the scheduler
    PENDING = "pending"         # Job is waiting for resources
    SCHEDULED = "scheduled"     # Job has been scheduled to a cluster
    RUNNING = "running"         # Job is running in a cluster
    COMPLETED = "completed"     # Job has completed successfully
    FAILED = "failed"           # Job has failed
    PREEMPTED = "preempted"     # Job has been preempted


class Job(BaseModel):
    id: str
    name: str
    username: str
    team: str
    status: JobStatus
    

