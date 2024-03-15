from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List

from beanie import PydanticObjectId

from model.message import Message


class IMessageService(metaclass=ABCMeta):
    @abstractmethod
    async def create_message(self, message: Message) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def get_message_by_id(self, message_id: PydanticObjectId) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def get_messages_by_conversation_id(self, conversation_id: PydanticObjectId) -> List[Message]:
        raise NotImplementedError

    @abstractmethod
    async def delete_message(self, message_id: PydanticObjectId) -> Message:
        raise NotImplementedError
