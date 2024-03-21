import json
from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from fastapi import WebSocket

from model.message import Message
from model.user import User
from service.auth_service import AuthService
from service.message_service import MessageService
from utils.nlp.evaluate import evaluateInput
from model.settings import settings

router = APIRouter(prefix="/message", tags=['Message'])

messages: List[Message] = []

message_service = MessageService()

auth_service = AuthService()


@router.get('/list', response_model=List[Message])
async def get_messages(conversation_id: PydanticObjectId, current_user: User = Depends(auth_service.get_current_user)):
    return await message_service.get_messages_by_conversation_id(conversation_id)


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        data = json.loads(data)
        message = data["text"]
        conv_id = data["conversationId"]
        res = evaluateInput(settings.searcher, settings.voc, message)
        await websocket.send_text(res)
        # await message_service.create_message(...)
        #
