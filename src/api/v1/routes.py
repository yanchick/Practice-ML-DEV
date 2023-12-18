import sys
from pathlib import Path
from fastapi import APIRouter


sys.path.append(str(Path(__file__).resolve().parents[2]))
from api.v1.endpoints.auth import router as auth_endpoint
from api.v1.endpoints.predict import router as predictions_endpoint


routers = [auth_endpoint, predictions_endpoint]

api_router = APIRouter(prefix="/api")

for router in routers:
    api_router.include_router(router)
