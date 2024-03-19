import os
from typing import List, Any

from beanie import init_beanie
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from controller.user_controller import router as user_router
from controller.conversation_controller import router as conversation_router
from controller.message_controller import router as message_controller
from model.conversation import Conversation
from model.message import Message

from model.user import User
from repository.base.db import MongoClient

app = FastAPI(
    title="ChatBotApp", openapi_url="/openapi.json"
)

app.mount("/css", StaticFiles(directory="template/css"), name="css")

BACKEND_CORS_ORIGINS: List[Any] = [
    "*"
]

root_router = APIRouter()

app.include_router(user_router)
app.include_router(conversation_router)
app.include_router(message_controller)
app.include_router(root_router)


@app.on_event("startup")
async def start_up_db_client():
    mongo = MongoClient(os.getenv("MONGO_URL"), os.getenv("MONGO_DB_NAME"))

    await init_beanie(database=mongo.client[mongo.database_name],
                      document_models=[User, Message, Conversation])


@app.get("/")
def index(request: Request) -> Any:
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the API</h1>"
        "<div>"
        "Check the docs: <a href='/docs'>here</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)


if BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
