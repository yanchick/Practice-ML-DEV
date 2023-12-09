from hashlib import md5

from service.api.schemas import UserLogin, UserRegister, SignInResponse, User
from service.api.repositories.base import AbstractRepository
from service.api.security import create_access_token
from service.api.models import DBUser
from service.api.repositories.user_repo import UserRepository



class AuthService:
    def __init__(self, users_repo: AbstractRepository):
        self.users_repo: AbstractRepository = users_repo()

    async def sing_in(self, user: UserLogin):

        db_user: DBUser = await self.users_repo.find_by_options(username=user.username, unique=True)

        if db_user is None:
            raise Exception("User not found")
        if db_user.hash_password != md5(user.password.encode('utf-8')).hexdigest():
            raise Exception("Password is incorrect")
        
        user: User = User(id=db_user.id, username=db_user.username)
        
        access_token = create_access_token(user)

        return SignInResponse(access_token=access_token,
                              user_info=User(id=db_user.id, 
                                             username=db_user.username))

    async def sign_up(self, user: UserRegister):

        db_user = await self.users_repo.find_by_options(username=user.username, unique=True)

        if db_user is not None:
            raise Exception("User already exists")
        
        user_id = await self.users_repo.add(data={"username": user.username, 
                                                  "hash_password": md5(user.password.encode('utf-8')).hexdigest(),
                                                  "user_email": user.email})
        
        user: User = User(id=user_id, username=user.username)
        
        access_token = create_access_token(user)

        return SignInResponse(access_token=access_token,
                              user_info=user)
    
def auth_service():
    return AuthService(UserRepository)
