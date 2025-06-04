from fastapi import APIRouter
from src.agents.responder import MODEL_REGISTRY, naive, list_models
from app.dataclass import model_query



models_router = APIRouter(prefix="/models")

@models_router.post("/response/")
def get_response_from_model(request:model_query):
    """Return the response from the correct model

    Args:
        request (model_query): The query model data

    Returns:
        json: response
    """
    model = MODEL_REGISTRY.get(request.model,naive)
    return model(request).process()    

@models_router.get("/models_list")
def root_fn():
    return list_models