from pydantic import BaseModel, field_validator, Field
from enum import Enum
from typing import Dict


class GPUTypes(str, Enum):
    A100 = "A100"
    H100 = "H100"
    H200 = "H200"


class Resource(BaseModel):
    # For example, {"A100": 2, "H100": 2} means that resource requires either 2 A100 GPUs or 2 H100 GPUs
    accepeted_gpu: Dict[GPUTypes, int]
    cpu: float = Field(gt=0, description="CPU in cores", default=2.0)
    memory_mb: float = Field(gt=0, description="Memory in MB", default=4096.0)
    disk_gb: float = Field(gt=0, description="Disk in GB", default=100.0)
    
    @field_validator('accepeted_gpu')
    def gpu_count_must_be_positive(cls, v: Dict[GPUTypes, int]) -> Dict[GPUTypes, int]:
        for gpu_type, count in v.items():
            if count <= 0:
                raise ValueError(f"GPU count for {gpu_type} must be positive")
        return v
    
    