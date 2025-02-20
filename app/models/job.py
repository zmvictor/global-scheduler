from pydantic import BaseModel, model_validator, Field
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


class Job(BaseModel):
    id: str                     
    username: str
    team: str               
    resource: Resource          
    replicas: int = 1           
    submitted_at: datetime
    last_updated_at: datetime      
    status: JobStatus
    preemption: bool = False           
    # Runtime fields can be added here
    # job_image: str
    # job_script: str
    # input_path: str
    # output_path: str
    
    # TODO: these values may only be obtainabled from JobManager since a job can be preempted multiple times
    def get_waiting_time(self) -> datetime:
        if self.status == JobStatus.SUBMITTED or self.status == JobStatus.PENDING:
            return datetime.now() - self.submitted_at
        if self.status == JobStatus.SCHEDULED:
            return self.last_updated_at - self.submitted_at
        # TODO: what if the job is preempted?
        return None
    
    def get_running_time(self) -> datetime:
        if self.status == JobStatus.RUNNING:
            return datetime.now() - self.last_updated_at
        # TODO: what if the job was running and then preempted and now running?
        return None

    def get_total_time(self) -> datetime:
        if self.status == JobStatus.COMPLETED or self.status == JobStatus.FAILED:
            return self.last_updated_at - self.submitted_at
        else:
            # TODO: what if the job is preempted?
            return datetime.now() - self.submitted_at
