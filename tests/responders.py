import pytest
import sys
from pathlib import Path


from src.agents.responder import MODEL_REGISTRY
from src.agents.base import model_query



# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def test_model_registry_not_empty():
    """Test that the model registry contains registered models"""
    assert len(MODEL_REGISTRY) > 0
    


sample_query = model_query(question="What is the purpose of life?",
                           model='any')

@pytest.mark.parametrize("model_name", MODEL_REGISTRY.keys())
def test_model_registry_processing(model_name):
    """Test all models in the registry for basic processing functionality"""
    try:
        # Get model class from registry
        model_class = MODEL_REGISTRY[model_name]
        
        # Initialize model with query
        model_instance = model_class(sample_query)
        
        # Process the query
        result = model_instance.cleaned()
        
        # Basic validation checks
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        
    except Exception as e:
        pytest.fail(f"Model {model_name} failed with error: {str(e)}")


