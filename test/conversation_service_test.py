import os
from datetime import datetime

import pytest
from beanie import PydanticObjectId
from bson import ObjectId

from model.conversation import Conversation

from repository.base.db import MongoClient
from repository.conversation_repository import ConversationRepository


@pytest.mark.asyncio
async def test_create_conversation():
    mongo = MongoClient(os.getenv("MONGO_URL"), os.getenv("MONGO_DB_NAME"))

    conversation_repository = ConversationRepository(mongo)
    await conversation_repository.init()

    mock_conversation_data = {
        "user_id": PydanticObjectId(ObjectId("65f2a99893f6cb312b5cae26")),
        "message_ids": []
    }

    # Create the mock Message object. Adjust according to how you'd use it with your repository
    mock_conversation = Conversation(**mock_conversation_data)

    result = await conversation_repository.create_conversation(mock_conversation)

    assert result.user_id == mock_conversation.user_id
    assert result.message_ids == []

