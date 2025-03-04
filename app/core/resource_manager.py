from abc import ABC, abstractmethod
from app.models.resource import Resource
from typing import Sequence, Optional, List, Dict


class ResourceManager(ABC):
    
    @abstractmethod
    def total_resource(self) -> Resource:
        pass
    
    @abstractmethod
    def total_allocatable_resource(self) -> Resource:
        pass
    
    @abstractmethod
    def resources(self) -> Sequence[Resource]:
        pass
    
    @abstractmethod
    def allocatable_resources(self) -> Sequence[Resource]:
        pass
    
    @abstractmethod
    def allocate_resource(self, resource: Resource) -> Optional[Resource]:
        pass
    
    @abstractmethod
    def release_resource(self, resource: Resource) -> Optional[Resource]:
        pass
