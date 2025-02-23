import pytest
from app.models.resource import Resource, GPUTypes

@pytest.fixture
def resource():
    return Resource(
        accepeted_gpu={GPUTypes.A100: 2, GPUTypes.H100: 2},
        cpu=2.0,
        memory_mb=4096.0,
        disk_gb=100.0
    )
    
def test_resource_creation(resource):
    assert resource.accepeted_gpu == {GPUTypes.A100: 2, GPUTypes.H100: 2}
    assert resource.cpu == 2.0
    assert resource.memory_mb == 4096.0
    assert resource.disk_gb == 100.0
    assert resource.is_valid() == True
    
def test_resource_addition(resource):
    other = Resource(
        accepeted_gpu={GPUTypes.A100: 1, GPUTypes.H200: 1},
        cpu=1.0,
        memory_mb=2048.0,
        disk_gb=50.0
    )
    result = resource + other
    assert result.accepeted_gpu == {GPUTypes.A100: 3, GPUTypes.H100: 2, GPUTypes.H200: 1}
    assert result.cpu == 3.0
    assert result.memory_mb == 6144.0
    assert result.disk_gb == 150.0
    assert result.is_valid() == True
    
def test_resource_subtraction(resource):
    other = Resource(
        accepeted_gpu={GPUTypes.A100: 1, GPUTypes.H100: 1},
        cpu=1.0,
        memory_mb=2048.0,
        disk_gb=50.0
    )
    result = resource - other
    assert result.accepeted_gpu == {GPUTypes.A100: 1, GPUTypes.H100: 1}
    assert result.cpu == 1.0
    assert result.memory_mb == 2048.0
    assert result.disk_gb == 50.0
    assert result.is_valid() == True
    
def test_resource_addition_invalid_type(resource):
    other = 1
    with pytest.raises(TypeError):
        _ = resource + other
    
def test_resource_subtraction_invalid_type(resource):
    other = 1
    with pytest.raises(TypeError):
        _ = resource - other
    
def test_resource_subtraction_invalid_value(resource):
    other = Resource(
        accepeted_gpu={GPUTypes.A100: 3, GPUTypes.H100: 1},
        cpu=1.0,
        memory_mb=2048.0,
        disk_gb=50.0
    )
    result = resource - other
    # result.accepeted_gpu == {GPUTypes.A100: -1, GPUTypes.H100: 1}
    assert result.is_valid() == True
    
    other.accepeted_gpu = {GPUTypes.A100: 3, GPUTypes.H100: 3}
    result = resource - other
    # result.accepeted_gpu == {GPUTypes.A100: -1, GPUTypes.H100: -1}
    assert result.is_valid() == False