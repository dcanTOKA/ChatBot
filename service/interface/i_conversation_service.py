from abc import ABCMeta, abstractmethod
from typing import Optional, List

from beanie import PydanticObjectId

from model.add_message import AddMessage
from model.conversation import Conversation


class IConversationService(metaclass=ABCMeta):

    @abstractmethod
    async def get_conversation_by_id(self, conversation_id: PydanticObjectId) -> Conversation:
        raise NotImplementedError

    @abstractmethod
    async def create_conversation(self, user_id: PydanticObjectId) -> Conversation:
        raise NotImplementedError

    @abstractmethod
    async def add_message_to_conversation(self, add_message_input: AddMessage) -> PydanticObjectId:
        raise NotImplementedError

    @abstractmethod
    async def get_conversations_by_user_id(self, user_id: PydanticObjectId, page=0, page_size=10) -> Optional[List[Conversation]]:
        raise NotImplementedError

    @abstractmethod
    async def delete_conversation(self, conversation_id: PydanticObjectId):
        raise NotImplementedError
