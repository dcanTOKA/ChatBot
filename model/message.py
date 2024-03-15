from datetime import datetime

from beanie import Document, PydanticObjectId
from pydantic import Field


class Message(Document):
    user_id: PydanticObjectId = Field(..., alias="userId")
    conversation_id: PydanticObjectId = Field(..., alias="conversationId")
    text: str = Field(..., alias="text")
    message_type: str = Field(..., alias="messageType")
    timestamp: datetime = Field(..., alias="timestamp")

    class Settings:
        name = "message"
