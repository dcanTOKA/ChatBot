from datetime import timedelta

from fastapi import HTTPException, status, Cookie
from fastapi.params import Depends
from starlette.requests import Request

from model.user import UserLogin
from repository.user_repository import UserRepository
from service.interface.i_auth_service import IAuthService
from service.user_service import UserService
from utils.custom_http import CustomHTTPBearer
from utils.jwt import JWTUtils


class AuthService(IAuthService):
    oauth2_scheme = CustomHTTPBearer()
    user_service = UserService()

    async def authenticate_user(self, user_data: UserLogin):
        user = await self.user_service.login_user(user_data)
        if not user:
            return False
        return user

    def create_token_for_user(self, user: UserLogin):
        access_token_expires = timedelta(minutes=JWTUtils.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = JWTUtils.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return access_token

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
        username = JWTUtils.verify_token(token, credentials_exception)
        user = await UserRepository.get_user_by_username(username)
        if user is None:
            raise credentials_exception
        return user
