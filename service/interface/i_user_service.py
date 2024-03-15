from abc import ABC, abstractmethod
from typing import Optional

from model.user import UserCreate, UserLogin, User


class IUserService(ABC):

    @staticmethod
    @abstractmethod
    async def create_user(user_data: UserCreate) -> User:
        raise NotImplemented

    @staticmethod
    @abstractmethod
    async def login_user(user_data: UserLogin) -> User:
        raise NotImplemented

    @staticmethod
    @abstractmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        raise NotImplemented

    @staticmethod
    @abstractmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        raise NotImplemented

    @staticmethod
    @abstractmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        raise NotImplemented
