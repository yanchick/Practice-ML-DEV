from fastapi import APIRouter

from src.repository.model import ModelRepository
from src.schemes.router import OpenAPIResponses, Session
from src.schemes.user_schemes import ModelListScheme, ModelScheme

router = APIRouter(prefix="/model", tags=["model"], responses=OpenAPIResponses.HTTP_401_UNAUTHORIZED)


@router.get("/")
async def get_models(session: Session) -> ModelListScheme:
    models = await ModelRepository.get_all_models(session)
    if models is None:
        return ModelListScheme(models=[])
    return ModelListScheme(
        models=[
            ModelScheme(
                id=model.id,
                name=model.name,
                cost=model.cost,
                description=model.description,
            )
            for model in models
        ]
    )
