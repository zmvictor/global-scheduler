from abc import ABC, abstractmethod
from app.models.resource import Resource
from typing import Any, Tuple, List, TypeAlias, Optional
import random

class ResourceManager(ABC):
    '''
    total_resources = available_resources + allocated_resources
    allocated_resources = preemptible_resources + non_preemptible_resources
    '''
    @abstractmethod
    def allocatable(self, resource: Resource) -> List[Any]:
        pass

    @abstractmethod
    def allocate(self, resource: Resource) -> Optional[Any]:
        pass

NodeResourceManager: TypeAlias = ResourceManager

class ClusterResourceManager(ResourceManager):
    def __init__(self, name: str, nodes: List[NodeResourceManager]):
        self._name = name,
        self._nodes = nodes
    
    def allocatable(self, resource: Resource) -> List[NodeResourceManager]:
        # TODO: Implement the logic to check if the resource is allocatable
        return []
    
    def allocate(self, resource: Resource) -> Optional[NodeResourceManager]:
        # TODO: Implement the logic to allocate the resource
        return None
    
    def name(self) -> str:
        return self._name
        

class GlobalResourceManager(ResourceManager):
    def __init__(self, clusters: List[ClusterResourceManager]):
        self._clusters = clusters
    
    def allocatable(self, resource: Resource) -> List[ClusterResourceManager]:
        clusters = list(filter(lambda cluster: cluster.allocatable(resource), self._clusters))
        return clusters
    
    def allocate(self, resource: Resource) -> Optional[ClusterResourceManager]:
        '''
        By default, we randomly select a cluster to allocate the resource
        '''
        clusters = self.allocatable(resource)
        if clusters:
            cluster = random.choice(clusters)
            cluster.allocate(resource)
            return cluster
        return None
    
    
    
    
    
    
    