from abc import ABC, abstractmethod
from app.models.resource import Resource
from typing import List, TypeAlias, Optional, Generic, TypeVar, Sequence, Tuple
import random

T = TypeVar('T')
ResourceReplica: TypeAlias = Tuple[Resource, int]

class ResourceManager(ABC, Generic[T]):
    '''
    total_resources = available_resources + allocated_resources
    allocated_resources = preemptible_resources + non_preemptible_resources
    '''
    @abstractmethod
    def allocatable(self, resource: Resource) -> Sequence[T]:
        '''
        Check if the resource is allocatable and return the list of alloctable slots in the resource manager
        '''
        pass

    @abstractmethod
    def allocate(self, resource: Resource) -> Optional[T]:
        '''
        Allocate the resource and return the slot where the resource is allocated
        '''
        pass
    
    @abstractmethod
    def allocatable(self, resources: List[ResourceReplica]) -> Sequence[T]:
        '''
        Check if the resources are allocatable and return the list of alloctable slots in the resource manager
        '''
        pass

    @abstractmethod
    def allocate(self, resources: List[ResourceReplica]) -> Optional[T]:
        '''
        Allocate the resources and return the slot where the resources are allocated
        '''
        pass

NodeResourceManager: TypeAlias = ResourceManager

class ClusterResourceManager(ResourceManager[NodeResourceManager]):
    def __init__(self, name: str, nodes: List[NodeResourceManager]):
        self._name = name,
        self._nodes = nodes
    
    def allocatable(self, resource: Resource) -> Sequence[NodeResourceManager]:
        alloctable_nodes = []

        for node in self._nodes:
            alloctable_nodes.extend(node.allocatable(resource))

        return alloctable_nodes

    def allocate(self, resource: Resource) -> Optional[NodeResourceManager]:
        alloctable_nodes = self.allocatable(resource)
        if alloctable_nodes:
            node = random.choice(alloctable_nodes)
            node.allocate(resource)
            return node
        return None
    
    def allocatable(self, resources: List[ResourceReplica]) -> Sequence[NodeResourceManager]:
        return NotImplemented

    def allocate(self, resources: List[ResourceReplica]) -> Optional[NodeResourceManager]:
        return NotImplemented
    
    def name(self) -> str:
        return self._name
        

class GlobalResourceManager(ResourceManager[ClusterResourceManager]):
    def __init__(self, clusters: List[ClusterResourceManager]):
        self._clusters = clusters
    
    def allocatable(self, resource: Resource) -> Sequence[ClusterResourceManager]:
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
    
    def allocatable(self, resources: List[ResourceReplica]) -> Sequence[ClusterResourceManager]:
        return NotImplemented
    
    def allocate(self, resources: List[ResourceReplica]) -> Optional[ClusterResourceManager]:
        return NotImplemented
    
    
    
    
    
    
    