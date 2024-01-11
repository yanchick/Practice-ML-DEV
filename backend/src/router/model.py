from fastapi import APIRouter

from src.schemes.router import OpenAPIResponses
from src.schemes.user_schemes import ModelListScheme, ModelScheme

router = APIRouter(prefix="/model", tags=["model"], responses=OpenAPIResponses.HTTP_401_UNAUTHORIZED)


@router.get("/")
async def get_models() -> ModelListScheme:
    return ModelListScheme(models=[ModelScheme(id=0, name="fake_model", description="fake_description", cost=0.0)])
