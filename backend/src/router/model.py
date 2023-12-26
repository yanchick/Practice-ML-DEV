from fastapi import APIRouter

from src.auth import CurrentUser
from src.schemes.router import OpenAPIResponses
from src.schemes.user_schemes import ModelListScheme, ModelScheme, PredictionItem, PredictionScheme

router = APIRouter(prefix="/model", tags=["model"], responses=OpenAPIResponses.HTTP_401_UNAUTHORIZED)


@router.get("/predict")
async def predict(model_id: int, user: CurrentUser) -> PredictionScheme:
    # user_dict = fake_users_db.get(form_data.username)
    # if user_dict:
    #     raise HTTPException(status_code=400, detail="Username already registered")
    # user = UserInDB(**user_dict)
    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    return PredictionScheme(predictions=[PredictionItem(result=0.0)])


@router.get("/")
async def get_models() -> ModelListScheme:
    return ModelListScheme(models=[ModelScheme(id=0, name="fake_model", description="fake_description", cost=0.0)])
