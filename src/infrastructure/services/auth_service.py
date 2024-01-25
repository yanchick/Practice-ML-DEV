from hashlib import md5

from src.api.schemas.auth_schema import UserLogin, UserRegister, UserLoginResponse, User
from src.infrastructure.repository.base_repository import AbstractRepository
from src.infrastructure.core.security import create_jwt_token
from src.infrastructure.database.model import Users
from src.infrastructure.repository.user_repository import UserRepository


class AuthService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def login(self, user: UserLogin):

        db_user: Users = await self.users_repo.find_by_options(username=user.username, unique=True)

        if db_user is None:
            raise Exception("User not found")
        if db_user.password != md5(user.password.encode('utf-8')).hexdigest():
            raise Exception("Password is incorrect")

        user: User = User(id=db_user.id, username=db_user.username)

        access_token = create_jwt_token(user)

        return UserLoginResponse(access_token=access_token,
                                 user_info=user)

    async def register(self, user: UserRegister):

        db_user = await self.users_repo.find_by_options(username=user.username, unique=True)

        if db_user is not None:
            raise Exception("User already exists")

        user_id = await self.users_repo.add(data={"username": user.username,
                                                  "password": md5(user.password.encode('utf-8')).hexdigest(),
                                                  "balance": 1000})

        user: User = User(id=user_id, username=user.username)

        access_token = create_jwt_token(user)

        return UserLoginResponse(access_token=access_token,
                                 user_info=user)

    async def get_balance(self, user: User):

        db_user = await self.users_repo.find_by_options(username=user.username, unique=True)
        if db_user is None:
            raise Exception("User not found")
        return {'balance': db_user.balance}


def get_auth_service():
    return AuthService(UserRepository)
