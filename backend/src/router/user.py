from fastapi import APIRouter, HTTPException, status

from src.auth import CurrentUser, authenticate_user, create_access_token, get_password_hash
from src.repository.user import UserRepository
from src.schemes.router import AuthFormData, OpenAPIResponses, Session
from src.schemes.user_schemes import SingUpRequest, Token, UserScheme

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/login")
async def login(form_data: AuthFormData, session: Session) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/signup")
async def signup(user_info: SingUpRequest, session: Session) -> Token:
    user = await UserRepository.get_user_by_username(user_info.username, session)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    hashed_password = get_password_hash(user_info.password)
    user = await UserRepository.create_user(
        username=user_info.username,
        password=hashed_password,
        session=session,
    )
    token = create_access_token(user.to_dict())
    return Token(access_token=token, token_type="bearer")


@router.get("/me", responses=OpenAPIResponses.HTTP_401_UNAUTHORIZED)
async def me(user: CurrentUser) -> UserScheme:
    return UserScheme(**user.to_dict())
