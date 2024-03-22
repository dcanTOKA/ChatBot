from typing import Optional, List

from beanie import PydanticObjectId

from model.add_message import AddMessage
from model.conversation import Conversation
from repository.conversation_repository import ConversationRepository
from service.interface.i_conversation_service import IConversationService


class ConversationService(IConversationService):

    def __init__(self):
        self.repository = ConversationRepository()

    async def get_conversation_by_id(self, conversation_id: PydanticObjectId) -> Conversation:
        return await self.repository.get_conversation_by_id(conversation_id)

    async def create_conversation(self, conversation: Conversation) -> Conversation:
        return await self.repository.create_conversation(conversation)

    async def add_message_to_conversation(self, add_message_input: AddMessage) -> PydanticObjectId:
        return await self.repository.add_message_to_conversation(add_message_input.conversation_id,
                                                                 add_message_input.message_id)

    async def get_conversations_by_user_id(self, user_id: PydanticObjectId, page=0, page_size=10) -> Optional[List[Conversation]]:
        return await self.repository.get_conversations_by_user_id(user_id, page, page_size)

    async def delete_conversation(self, conversation_id: PydanticObjectId):
        return await self.repository.delete_conversation(conversation_id)
