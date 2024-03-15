from typing import Optional

from beanie import init_beanie

from model.user import User

from .interface.i_user_repository import IUserRepository
from .base.db import MongoClient


class UserRepository(IUserRepository):

    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client

    async def init(self):
        db_instance = self.mongo_client.client[self.mongo_client.database_name]

        await init_beanie(database=db_instance,
                          document_models=[User])

    @staticmethod
    async def create_user(user: User) -> User:
        await User.insert_one(user)
        return user

    @staticmethod
    async def update_user(user_id: str, updated_user: User) -> User:
        user = await User.get(user_id)

        if user:
            for key, value in updated_user.items():
                setattr(user, key, value)
            await user.save()

        return user

    @staticmethod
    async def delete_user(user_id: str) -> bool:
        user = await User.get(user_id)
        if user:
            await user.delete()
            return True

        return False

    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        return await User.get(user_id)

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        return await User.find_one(User.username == username)

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        return await User.find_one(User.email == email)
