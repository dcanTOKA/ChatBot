from fastapi import APIRouter, HTTPException, status, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response, RedirectResponse
from starlette.templating import Jinja2Templates

from model.auth import Auth
from model.user import User, UserCreate
from model.user import UserLogin
from service.auth_service import AuthService
from service.user_service import UserService

router = APIRouter(prefix='/account', tags=['Account'])

auth_service = AuthService()

templates = Jinja2Templates(directory="template")


@router.post('/register', response_model=User)
async def register_to_app(user_data: UserCreate) -> User:
    existing_user = await UserService.get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    existing_email = await UserService.get_user_by_email(user_data.email)
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    created_user = await UserService.create_user(user_data)
    if created_user:
        return created_user
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User could not be created")


@router.post("/login")
async def login(form_data: UserLogin) -> Auth:
    user = await auth_service.authenticate_user(form_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await auth_service.create_token_for_user(user)

    auth = Auth(access_token=access_token)

    return auth
