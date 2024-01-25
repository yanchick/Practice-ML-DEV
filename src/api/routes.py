from fastapi import APIRouter

from src.api.endpoints.auth import router as auth_endpoint
from src.api.endpoints.predict import router as predictions_endpoint


routers = [auth_endpoint, predictions_endpoint]

api_router = APIRouter()

for router in routers:
    api_router.include_router(router)
