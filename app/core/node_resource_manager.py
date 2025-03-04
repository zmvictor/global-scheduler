from app.models.resource import Resource
from app.core.resource_manager import ResourceManager
from typing import Sequence, Optional


class NodeResourceManager(ResourceManager):
    def __init__(self, total_resource: Resource):
        self._total_resource = total_resource
        self._allocatable_resource = total_resource.model_copy()
    
    def total_resource(self) -> Resource:
        return self._total_resource
    
    def total_allocatable_resource(self) -> Resource:
        return self._allocatable_resource
    
    def resources(self) -> Sequence[Resource]:
        return [self._total_resource]
    
    def allocatable_resources(self) -> Sequence[Resource]:
        return [self._allocatable_resource]
    
    def allocate_resource(self, resource: Resource) -> Optional[Resource]:
        delta_resource = self._allocatable_resource - resource
        if delta_resource.is_valid():
            delta_resource.id = self._allocatable_resource.id
            self._allocatable_resource = delta_resource
            return self._allocatable_resource
        else:
            return None
        
    def release_resource(self, resource: Resource) -> Optional[Resource]:
        new_allocated_resource = self._allocatable_resource + resource
        delta_resource = self._total_resource - new_allocated_resource
        if delta_resource.is_valid():
            new_allocated_resource.id = self._allocatable_resource.id
            self._allocatable_resource = new_allocated_resource
            return self._allocatable_resource
        else:
            return None