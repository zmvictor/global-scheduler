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
    name: str                   
    username: str               
    resource: Resource          
    replicas: int = 1           
    submitted_at: datetime      
    status: JobStatus           
    priority: int = Field(ge=0, le=100, description="Job priority (0-100)")
    job_image: str
    job_script: str
    input_path: str
    output_path: str
    
    @model_validator(pre=True)
    def validate_resource(cls, v):
        if not v.accepeted_gpu:
            raise ValueError("Resource must have at least one GPU type")
        return v
    

class JobRecord(BaseModel):
    id: str                     # Unique identifier for the job
    status: JobStatus           # Status of the job
    last_updated: datetime      # Time when the job status was last updated
    

