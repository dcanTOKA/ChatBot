from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends

from model.add_message import AddMessage
from model.conversation import Conversation
from model.user import User
from service.auth_service import AuthService
from service.conversation_service import ConversationService

router = APIRouter(prefix="/conversation", tags=['Conversation'])

conversation_service = ConversationService()

auth_service = AuthService()


@router.post("/", response_model=Conversation)
async def create_conversation(conversation: Conversation, current_user: User = Depends(auth_service.get_current_user)):
    return await conversation_service.create_conversation(conversation)


@router.get("/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: PydanticObjectId, current_user: User = Depends(auth_service.get_current_user)):
    conversation = await conversation_service.get_conversation_by_id(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post("/{conversation_id}/messages", response_model=Conversation)
async def add_message_to_conversation(add_message_form: AddMessage, current_user: User = Depends(auth_service.get_current_user)):
    return await conversation_service.add_message_to_conversation(add_message_form)


@router.delete("/{conversation_id}/messages/{message_id}")
async def remove_message_from_conversation(conversation_id: PydanticObjectId, current_user: User = Depends(auth_service.get_current_user)):
    return await conversation_service.delete_conversation(conversation_id)


@router.get("/", response_model=List[Conversation])
async def list_conversations(user_id: PydanticObjectId, page: int = 0, page_size: int = 10, current_user: User = Depends(auth_service.get_current_user)):
    return await conversation_service.get_conversations_by_user_id(user_id, page, page_size)
