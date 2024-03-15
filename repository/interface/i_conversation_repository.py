from abc import ABCMeta, abstractmethod
from typing import Optional, List

from beanie import PydanticObjectId

from model.conversation import Conversation
from model.message import Message


class IConversationRepository(metaclass=ABCMeta):

    @abstractmethod
    async def create_conversation(self, conversation: Conversation) -> Conversation:
        raise NotImplementedError

    @abstractmethod
    async def get_conversation_by_id(self, conversation_id: PydanticObjectId) -> Optional[Conversation]:
        raise NotImplementedError

    @abstractmethod
    async def get_conversations_by_user_id(self, user_id: PydanticObjectId) -> Optional[List[Conversation]]:
        raise NotImplementedError

    @abstractmethod
    async def add_message_to_conversation(self, conversation_id: PydanticObjectId, message_id: PydanticObjectId) -> PydanticObjectId:
        raise NotImplementedError

    @abstractmethod
    async def delete_conversation(self, conversation_id: PydanticObjectId):
        raise NotImplementedError


