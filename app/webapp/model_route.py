from fastapi import APIRouter

from src.agents.responder import list_models, get_response
from app.webapp.dataclass import model_query


models_router = APIRouter(prefix="/models")


@models_router.post("/response/")
async def get_response_from_model(request: model_query):
    """Return the response from the correct model

    Args:
        request (model_query): The query model data

    Returns:
        json: response
    """
    response = await get_response(request)
    return response


@models_router.get("/models_list")
def getList():
    """Get the list of models present

    Returns:
        _type_: _description_
    """
    return list_models
