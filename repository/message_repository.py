from datetime import datetime
from typing import List

from beanie import PydanticObjectId, init_beanie

from model.conversation import Conversation
from model.message import Message
from repository.base.db import MongoClient
from repository.interface.i_message_repository import IMessageRepository


class MessageRepository(IMessageRepository):

    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client

    async def init(self):
        db_instance = self.mongo_client.client[self.mongo_client.database_name]

        await init_beanie(database=db_instance,
                          document_models=[Message, Conversation])

    async def create_message(self, message: Message) -> Message:
        return await Message.insert(message)

    async def get_message_by_id(self, message_id: PydanticObjectId) -> Message:
        return await Message.get(message_id)

    async def get_messages_by_conversation_id(self, conversation_id: PydanticObjectId) -> List[Message]:
        return await Message.find(Message.conversation_id == conversation_id).to_list()

    async def delete_message(self, message_id: PydanticObjectId):
        message = await Message.get(message_id)
        if message:
            await message.delete()
