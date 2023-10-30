from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router

routers = APIRouter()
router_list = [auth_router, post_router, tag_router, user_router]

for router in router_list:
    router.tags = routers.tags.append("v1")
    routers.include_router(router)
