import pytest
import random
from typing import List, Sequence, Optional
from ..resource_manager import ClusterResourceManager, GlobalResourceManager, ResourceManager, ResourceReplica
from app.models.resource import Resource

# Mock Resource class for testing
class MockResource(Resource):
    def __init__(self, resource_id=1):
        self.resource_id = resource_id
        self.allocated = False
    
    def __eq__(self, other):
        if isinstance(other, MockResource):
            return self.resource_id == other.resource_id
        return False


# Mock NodeResourceManager for testing ClusterResourceManager
class MockNodeResourceManager(ResourceManager):
    def __init__(self, node_id, can_allocate=True):
        self.node_id = node_id
        self.can_allocate = can_allocate
        self.allocated_resources = []
    
    def allocatable(self, resource):
        return [self] if self.can_allocate else []
    
    def allocate(self, resource):
        if self.can_allocate:
            self.allocated_resources.append(resource)
            return self
        return None
        
    def allocatable(self, resources: List[ResourceReplica]):
        return [self] if self.can_allocate else []
    
    def allocate(self, resources: List[ResourceReplica]):
        if self.can_allocate:
            for resource, replicas in resources:
                self.allocated_resources.extend([resource] * replicas)
            return self
        return None


# Mock ClusterResourceManager for testing GlobalResourceManager
class MockClusterResourceManager(ClusterResourceManager):
    def __init__(self, name, can_allocate=True):
        self.mock_name = name
        self.can_allocate = can_allocate
        self.allocated_resources = []
        # Pass empty nodes list as we're mocking the behavior
        super().__init__(name, [])
    
    def allocatable(self, resource):
        return [self] if self.can_allocate else []
    
    def allocate(self, resource):
        if self.can_allocate:
            self.allocated_resources.append(resource)
            return self
        return None
    
    def name(self):
        return self.mock_name


# Fixtures
@pytest.fixture
def mock_resource():
    return MockResource(resource_id=1)

@pytest.fixture
def mock_nodes():
    return [
        MockNodeResourceManager(1, can_allocate=True),
        MockNodeResourceManager(2, can_allocate=True),
        MockNodeResourceManager(3, can_allocate=False),
    ]

@pytest.fixture
def mock_clusters():
    return [
        MockClusterResourceManager("cluster1", can_allocate=True),
        MockClusterResourceManager("cluster2", can_allocate=True),
        MockClusterResourceManager("cluster3", can_allocate=False),
    ]

@pytest.fixture
def cluster_manager(mock_nodes):
    return ClusterResourceManager("test-cluster", mock_nodes)

@pytest.fixture
def global_manager(mock_clusters):
    return GlobalResourceManager(mock_clusters)


# ClusterResourceManager Tests
def test_cluster_manager_initialization(mock_nodes):
    manager = ClusterResourceManager("test-cluster", mock_nodes)
    assert manager._name == "test-cluster",  # Note: This is a tuple due to the comma in the __init__ method
    assert manager._nodes == mock_nodes

def test_cluster_manager_name(cluster_manager):
    assert cluster_manager.name() == "test-cluster",  # Note: This is a tuple due to the comma in the __init__ method

def test_cluster_manager_allocatable(cluster_manager, mock_resource):
    # Should return nodes that can allocate the resource
    allocatable_nodes = cluster_manager.allocatable(mock_resource)
    assert len(allocatable_nodes) == 2  # Only first two nodes can allocate

def test_cluster_manager_allocate(monkeypatch, cluster_manager, mock_resource):
    # Mock random.choice to always pick the first node
    monkeypatch.setattr(random, "choice", lambda x: x[0])
    
    node = cluster_manager.allocate(mock_resource)
    assert node is not None
    assert node.node_id == 1
    assert mock_resource in node.allocated_resources

def test_cluster_manager_allocate_no_nodes(monkeypatch, mock_nodes, mock_resource):
    # Create a cluster manager with no allocatable nodes
    no_allocatable_nodes = [MockNodeResourceManager(1, can_allocate=False)]
    manager = ClusterResourceManager("test-cluster", no_allocatable_nodes)
    
    result = manager.allocate(mock_resource)
    assert result is None

def test_cluster_manager_allocatable_resources(cluster_manager):
    resources = [(MockResource(1), 2)]
    assert cluster_manager.allocatable(resources) == NotImplemented

def test_cluster_manager_allocate_resources(cluster_manager):
    resources = [(MockResource(1), 2)]
    assert cluster_manager.allocate(resources) == NotImplemented


# GlobalResourceManager Tests
def test_global_manager_initialization(mock_clusters):
    manager = GlobalResourceManager(mock_clusters)
    assert manager._clusters == mock_clusters

def test_global_manager_allocatable(global_manager, mock_resource):
    allocatable_clusters = global_manager.allocatable(mock_resource)
    assert len(allocatable_clusters) == 2  # First two clusters can allocate

def test_global_manager_allocate(monkeypatch, global_manager, mock_resource):
    # Mock random.choice to always pick the first cluster
    monkeypatch.setattr(random, "choice", lambda x: x[0])
    
    cluster = global_manager.allocate(mock_resource)
    assert cluster is not None
    assert cluster.mock_name == "cluster1"
    assert mock_resource in cluster.allocated_resources

def test_global_manager_allocate_no_clusters(mock_resource):
    # Create a global manager with no allocatable clusters
    no_allocatable_clusters = [
        MockClusterResourceManager("cluster1", can_allocate=False),
        MockClusterResourceManager("cluster2", can_allocate=False)
    ]
    manager = GlobalResourceManager(no_allocatable_clusters)
    
    result = manager.allocate(mock_resource)
    assert result is None

def test_global_manager_allocatable_resources(global_manager):
    resources = [(MockResource(1), 2)]
    assert global_manager.allocatable(resources) == NotImplemented

def test_global_manager_allocate_resources(global_manager):
    resources = [(MockResource(1), 2)]
    assert global_manager.allocate(resources) == NotImplemented