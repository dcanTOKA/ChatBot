import os
from datetime import datetime

import pytest
from beanie import PydanticObjectId
from bson import ObjectId

from model.message import Message

from repository.base.db import MongoClient
from repository.conversation_repository import ConversationRepository
from repository.message_repository import MessageRepository


@pytest.mark.asyncio
async def test_create_message():
    mongo = MongoClient(os.getenv("MONGO_URL"), os.getenv("MONGO_DB_NAME"))

    message_repository = MessageRepository(mongo)
    conversation_repository = ConversationRepository(mongo)
    await message_repository.init()

    mock_message_data = {
        "user_id": PydanticObjectId(ObjectId("65f2a99893f6cb312b5cae24")),  # Generate a new ObjectId for the user
        "conversation_id": PydanticObjectId(ObjectId("65f2c4fab8defcafcfa168e6")),
        # Generate a new ObjectId for the conversation
        "text": "Hello, this is a mock message!",
        "message_type": "user",  # Assuming "user" is a valid message type in your schema
        "timestamp": datetime.utcnow(),
    }

    # Create the mock Message object. Adjust according to how you'd use it with your repository
    mock_message = Message(**mock_message_data)

    result = await message_repository.create_message(mock_message)
    added_message_id = await conversation_repository.add_message_to_conversation(result.conversation_id, result.id)

    assert result.user_id == mock_message.user_id
    assert result.text == mock_message.text

    conv = await conversation_repository.get_conversation_by_id(result.conversation_id)

    assert conv.message_ids == [added_message_id]


@pytest.mark.asyncio
async def test_add_message_to_conversation():
    mongo = MongoClient(os.getenv("MONGO_URL"), os.getenv("MONGO_DB_NAME"))

    message_repository = MessageRepository(mongo)
    conversation_repository = ConversationRepository(mongo)
    await message_repository.init()

    mock_message_data = {
        "user_id": PydanticObjectId(ObjectId("65f2a99893f6cb312b5cae26")),
        "conversation_id": PydanticObjectId(ObjectId("65f2c4fab8defcafcfa168e6")),
        "text": "Hello, what can I do for you?",
        "message_type": "bot",
        "timestamp": datetime.utcnow(),
    }

    mock_message = Message(**mock_message_data)

    result = await message_repository.create_message(mock_message)
    added_message_id = await conversation_repository.add_message_to_conversation(result.conversation_id, result.id)

    assert result.user_id == mock_message.user_id
    assert result.text == mock_message.text

    conv = await conversation_repository.get_conversation_by_id(result.conversation_id)

    assert added_message_id in conv.message_ids
