from app.models.resource import Resource
from app.core.resource_manager import ResourceManager
from app.core.node_resource_manager import NodeResourceManager
from typing import Sequence, Optional, List, Dict
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ClusterResourceManager(ResourceManager):
    def __init__(self, node_resource_managers: List[NodeResourceManager]):
        self._node_resource_managers: Dict[str, NodeResourceManager] = {}
        for i, node_rs in enumerate(node_resource_managers):
            node_id = node_rs.total_resource().id
            if not node_id:
                raise ValueError(f"NodeResourceManager at index {i} does not have an id")
            if node_id in self._node_resource_managers:
                raise ValueError(f"NodeResourceManager at index {i} has a duplicate id: {node_id}")
            self._node_resource_managers[node_id] = node_rs
        
    def add_node(self, node_resource_manager: NodeResourceManager) -> bool:
        node_id = node_resource_manager.total_resource().id
        if not node_id:
            logger.error("NodeResourceManager does not have an id")
            return False
        if node_id in self._node_resource_managers:
            logger.error(f"NodeResourceManager has a duplicate id: {node_id}")
            return False
        self._node_resource_managers[node_id] = node_resource_manager
        return True
    
    def delete_node(self, node_id: str) -> bool:
        if node_id not in self._node_resource_managers:
            logger.error(f"NodeResourceManager with id {node_id} does not exist")
            return False
        _ = self._node_resource_managers.pop(node_id)
        return True
    
    def total_resource(self) -> Resource:
        return sum([node_rs.total_resource() for node_rs in self._node_resource_managers.values()])
    
    def total_allocatable_resource(self) -> Resource:
        return sum([node_rs.total_allocatable_resource() for node_rs in self._node_resource_managers.values()])
    
    def resources(self) -> Sequence[Resource]:
        return [node_rs.total_resource() for node_rs in self._node_resource_managers.values()]
    
    def allocatable_resources(self) -> Sequence[Resource]:
        return [node_rs.total_allocatable_resource() for node_rs in self._node_resource_managers.values()]
        
    def allocate_resource(self, resource: Resource) -> Optional[Resource]:
        '''
        Pick the first node that can allocate the resource if there is one
        '''
        for node_rs in self._node_resource_managers.values():
            new_allocatable_resource = node_rs.allocate_resource(resource)
            if new_allocatable_resource:
                return new_allocatable_resource
        return None
    
    def release_resource(self, resource: Resource) -> Optional[Resource]:
        '''
        Find the node that has the resource and release it
        '''
        if not resource.id:
            logger.error("Resource does not have an id")
            return None
        if resource.id not in self._node_resource_managers:
            logger.error(f"Resource with id {resource.id} does not exist")
            return None
        
        node_rs = self._node_resource_managers[resource.id]
        new_allocatable_resource = node_rs.release_resource(resource)
        return new_allocatable_resource
