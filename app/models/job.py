from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime
from app.models.resource import Resource


class JobStatus (str, Enum):
    SUBMITTED = "submitted"     # Job has been submitted to the scheduler
    PENDING = "pending"         # Job is waiting for resources
    SCHEDULED = "scheduled"     # Job has been scheduled to a cluster
    RUNNING = "running"         # Job is running in a cluster
    COMPLETED = "completed"     # Job has completed successfully
    FAILED = "failed"           # Job has failed
    PREEMPTED = "preempted"     # Job has been preempted
    TERMINATED = "terminated"   # Job has been terminated by the user


class Job(BaseModel):
    id: str                     
    username: str
    team: str               
    resource: Resource          
    replicas: int = 1           
    submitted_at: datetime
    status: JobStatus
    preemption: bool = False
    preemption_count: int = 0           
    # Runtime fields can be added here
    # job_image: str
    # job_script: str
    # input_path: str
    # output_path: str
    
    
