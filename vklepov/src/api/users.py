from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers, BaseUserManager, IntegerIDMixin
from fastapi_users.authentication import (
    CookieTransport,
    JWTStrategy,
    AuthenticationBackend,
)
from . import models, schemas

SECRET = "SECRET"
LIFETIME = 3600
WELCOME_BONUS = 100_00
cookie_transport = CookieTransport(cookie_max_age=LIFETIME)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=LIFETIME)


auth_backend = AuthenticationBackend(
    name="cookie-jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[models.User, int]):
    pass


async def get_user_manager(user_db=Depends(models.get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[models.User, int](
    get_user_manager,
    [auth_backend],
)


user_router = APIRouter()

user_router.include_router(
    fastapi_users.get_register_router(schemas.UserRead, schemas.UserCreate),
    prefix="/user",
    tags=["auth"],
)

user_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()
