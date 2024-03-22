from typing import Optional, List, Union

from beanie import PydanticObjectId, init_beanie

from model.conversation import Conversation
from model.message import Message
from repository.base.db import MongoClient
from repository.interface.i_conversation_repository import IConversationRepository


class ConversationRepository(IConversationRepository):
    def __init__(self, mongo_client: Union[MongoClient, None] = None):
        self.mongo_client = mongo_client

    async def init(self):
        db_instance = self.mongo_client.client[self.mongo_client.database_name]

        await init_beanie(database=db_instance,
                          document_models=[Conversation, Message])

    async def create_conversation(self, conversation: Conversation) -> Conversation:
        return await Conversation.insert(conversation)

    async def get_conversation_by_id(self, conversation_id: PydanticObjectId) -> Optional[Conversation]:
        conversation = await Conversation.get(conversation_id)
        return conversation

    async def get_conversations_by_user_id(self, user_id: PydanticObjectId, page: int, page_size: int) -> Optional[List[Conversation]]:
        skip = (page - 1) * page_size
        conversations = await Conversation.find(Conversation.user_id == user_id).skip(skip).limit(page_size).to_list()
        return conversations

    async def add_message_to_conversation(self, conversation_id: PydanticObjectId,
                                          message_id: PydanticObjectId) -> PydanticObjectId:
        conversation = await Conversation.get(conversation_id)
        if conversation:
            conversation.message_ids.append(message_id)
            await conversation.save()

            return message_id

    async def delete_conversation(self, conversation_id: PydanticObjectId) -> PydanticObjectId:
        conversation = await Conversation.get(conversation_id)
        if conversation:
            await conversation.delete()
            return conversation_id
