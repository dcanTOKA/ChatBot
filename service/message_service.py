import os
from datetime import datetime
from typing import List

from beanie import PydanticObjectId

from model.message import Message
from repository.base.db import MongoClient
from service.interface.i_message_service import IMessageService
from repository.message_repository import MessageRepository


class MessageService(IMessageService):
    def __init__(self):
        self.repository = MessageRepository(MongoClient(os.getenv("MONGO_URL"), os.getenv("MONGO_DB_NAME")))

    async def create_message(self, message: Message) -> Message:
        return await self.repository.create_message(message)

    async def get_message_by_id(self, message_id: PydanticObjectId) -> Message:
        return await self.repository.get_message_by_id(message_id)

    async def get_messages_by_conversation_id(self, conversation_id: PydanticObjectId) -> List[Message]:
        return await self.repository.get_messages_by_conversation_id(conversation_id)

    async def delete_message(self, message_id: PydanticObjectId) -> Message:
        return await self.repository.delete_message(message_id)
