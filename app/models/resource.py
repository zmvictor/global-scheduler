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
    
    def is_valid(self) -> bool:
        for count in self.accepeted_gpu.values():
            if count < 0:
                return False
        return self.cpu >= 0 and self.memory_mb >= 0 and self.disk_gb >= 0

    # TODO: Resource should support addition and subtraction
    def __add__(self, other: "Resource") -> "Resource":
        if not isinstance(other, Resource):
            return NotImplemented

        accepeted_gpu = self.accepeted_gpu.copy()
        for gpu_type, count in other.accepeted_gpu.itmes():
            if gpu_type in accepeted_gpu:
                accepeted_gpu[gpu_type] += count
            else:
                accepeted_gpu[gpu_type] = count

        return Resource(
            accepeted_gpu = accepeted_gpu,
            cpu = self.cpu + other.cpu,
            memory_mb = self.memory_mb + other.memory_mb,
            disk_gb = self.disk_gb + other.disk_gb
        )
        
    
    def __sub__(self, other: "Resource") -> "Resource":
        if not isinstance(other, Resource):
            return NotImplemented
        
        accepeted_gpu = self.accepeted_gpu.copy()
        for gpu_type, count in other.accepeted_gpu.itmes():
            if gpu_type in accepeted_gpu:
                accepeted_gpu[gpu_type] -= count
            else:
                accepeted_gpu[gpu_type] = -count
        
        return Resource(
            accepeted_gpu = accepeted_gpu,
            cpu = self.cpu - other.cpu,
            memory_mb = self.memory_mb - other.memory_mb,
            disk_gb = self.disk_gb - other.disk_gb
        )