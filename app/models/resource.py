from pydantic import BaseModel
from enum import Enum
from typing import Dict


class GPUTypes(str, Enum):
    A100 = "A100"
    H100 = "H100"
    H200 = "H200"


class Resource(BaseModel):
    # For example, {"A100": 2, "H100": 2} means that resource requires either 2 A100 GPUs or 2 H100 GPUs
    accepeted_gpu: Dict[GPUTypes, int]
    cpu: float = 4.0
    memory_mb: float = 4096.0
    disk_gb: float = 100.0