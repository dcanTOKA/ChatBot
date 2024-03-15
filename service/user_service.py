from typing import Optional

from model.user import UserLogin, User, UserCreate
from service.interface.i_user_service import IUserService
from utils.security import hash_password, verify_password
from repository.user_repository import UserRepository


class UserService(IUserService):

    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        return await UserRepository.get_user_by_id(user_id)

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        return await UserRepository.get_user_by_username(username)

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        return await UserRepository.get_user_by_email(email)

    @staticmethod
    async def create_user(user_data: UserCreate) -> User:
        username_exist = await UserRepository.get_user_by_username(user_data.username)
        email_exist = await UserRepository.get_user_by_email(user_data.email)

        if not (username_exist or email_exist):
            hashed_password = hash_password(user_data.password)

            new_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_password)

            created_user = await UserRepository.create_user(user=new_user)

            if created_user.id:
                return created_user

    @staticmethod
    async def login_user(user_data: UserLogin) -> Optional[User]:
        user = await UserRepository.get_user_by_username(user_data.username)

        if user and verify_password(user_data.password, user.hashed_password):
            return user

        return None

