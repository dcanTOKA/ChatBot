from beanie import Document
from pydantic import BaseModel, EmailStr, Field


class User(Document):
    username: str = Field(..., alias="username")
    email: str = Field(..., alias="email")
    hashed_password: str = Field(..., alias="hashedPassword")

    class Settings:
        name = "users"


class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    email: EmailStr
