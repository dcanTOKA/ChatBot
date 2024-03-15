from abc import ABC, abstractmethod
from typing import Optional
from model.user import User


class IUserRepository(ABC):

    @staticmethod
    @abstractmethod
    async def create_user(user: User) -> User:
        raise NotImplemented

    @staticmethod
    @abstractmethod
    async def update_user(user_id: str, updated_user: User) -> User:
        raise NotImplemented

    @staticmethod
    @abstractmethod
    async def delete_user(user_id: str):
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
    async def get_user_by_email(username: str) -> Optional[User]:
        raise NotImplemented
