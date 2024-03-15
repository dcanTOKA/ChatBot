from beanie import PydanticObjectId
from pydantic import BaseModel


class AddMessage(BaseModel):
    message_id: PydanticObjectId
    conversation_id: PydanticObjectId
