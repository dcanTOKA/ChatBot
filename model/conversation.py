from typing import List

from beanie import Document, PydanticObjectId
from pydantic import Field


class Conversation(Document):
    user_id: PydanticObjectId = Field(..., alias="userId")
    message_ids: List[PydanticObjectId] = Field(..., alias="messageIds")

    class Settings:
        name = "conversation"
