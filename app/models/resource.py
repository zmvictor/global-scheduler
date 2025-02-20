from pydantic import BaseModel
from enum import Enum
from typing import Dict


class GPUTypes(str, Enum):
    A100 = "A100"
    H100 = "H100"
    H200 = "H200"


class Resource(BaseModel):
    gpu: Dict[GPUTypes, int]
    cpu: float
    memory_mb: float
    disk_gb: float