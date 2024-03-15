from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Body
from typing import List

from model.add_message import AddMessage
from model.conversation import Conversation  # Assuming you have a Conversation model defined
from service.conversation_service import ConversationService  # Adjust import based on your project structure

router = APIRouter(prefix="/conversation")

conversation_service = ConversationService()


@router.post("/", response_model=Conversation)
async def create_conversation(conversation: Conversation):
    return await conversation_service.create_conversation(conversation)


@router.get("/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: PydanticObjectId):
    conversation = await conversation_service.get_conversation_by_id(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post("/{conversation_id}/messages", response_model=Conversation)
async def add_message_to_conversation(add_message_form: AddMessage):
    return await conversation_service.add_message_to_conversation(add_message_form)


@router.delete("/{conversation_id}/messages/{message_id}")
async def remove_message_from_conversation(conversation_id: PydanticObjectId):
    return await conversation_service.delete_conversation(conversation_id)


@router.get("/", response_model=List[Conversation])
async def list_conversations(user_id: PydanticObjectId):
    return await conversation_service.get_conversations_by_user_id(user_id)
