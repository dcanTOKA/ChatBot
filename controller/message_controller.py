from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from fastapi import WebSocket

from model.message import Message
from model.user import User
from service.auth_service import AuthService
from service.message_service import MessageService

router = APIRouter(prefix="/message", tags=['Message'])

messages: List[Message] = []

message_service = MessageService()

auth_service = AuthService()


@router.get('/list', response_model=List[Message])
async def get_messages(conversation_id: PydanticObjectId, current_user: User = Depends(auth_service.get_current_user)):
    return await message_service.get_messages_by_conversation_id(conversation_id)


@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Burada gelen mesajı işleyip, seq2seq veya LLM modeline gönderebilirsiniz.
        await websocket.send_text(f"Mesajınız alındı: {data}")
        # await message_service.create_message(...)
