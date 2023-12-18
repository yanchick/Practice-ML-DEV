import sys
from pathlib import Path

from hashlib import md5


sys.path.append(str(Path(__file__).resolve().parents[2]))
from api.v1.schemas.auth_schema import UserLogin, UserRegister, UserLoginResponse, User
from infrastructure.repository.base_repository import AbstractRepository
from infrastructure.core.security import create_jwt_token
from infrastructure.database.model import Users
from infrastructure.repository.user_repository import UserRepository



class AuthService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def login(self, user: UserLogin):

        db_user: Users = await self.users_repo.find_by_options(name=user.name, unique=True)

        if db_user is None:
            raise Exception("User not found")
        if db_user.hash_password != md5(user.password.encode('utf-8')).hexdigest():
            raise Exception("Password is incorrect")

        user: User = User(id=db_user.id, name=db_user.name)

        access_token = create_jwt_token(user)

        return UserLoginResponse(access_token=access_token,
                                 user_info=user)

    async def register(self, user: UserRegister):

        db_user = await self.users_repo.find_by_options(name=user.name, unique=True)

        if db_user is not None:
            raise Exception("User already exists")

        user_id = await self.users_repo.add(data={"name": user.name, 
                                                  "hash_password": md5(user.password.encode('utf-8')).hexdigest(),
                                                  "user_email": user.email})

        user: User = User(id=user_id, name=user.name)

        access_token = create_jwt_token(user)

        return UserLoginResponse(access_token=access_token,
                                 user_info=user)

def get_auth_service():
    return AuthService(UserRepository)
