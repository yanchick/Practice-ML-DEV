from fastapi import APIRouter
from api.v1.endpoints.auth import router as auth_router
from api.v1.endpoints.models import router as models_router
from api.v1.endpoints.predictor import router as predictor_router

routers = APIRouter()
router_list = [auth_router, models_router, predictor_router]

for router in router_list:
    router.tags = routers.tags.append("v1")
    routers.include_router(router)

