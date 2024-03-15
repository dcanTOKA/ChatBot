from fastapi import APIRouter, HTTPException, Body, Path
from datetime import datetime
from typing import List

from enums.message_type import MessageType
from model.message import Message  # Assuming you have a models.py file with Message and MessageType defined
from service.message_service import MessageService  # Adjust the import based on your project structure

router = APIRouter(prefix="/messages")

# Assuming you have an instance of MessageService
message_service = MessageService()
