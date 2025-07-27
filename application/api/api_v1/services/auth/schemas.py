from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserReg(BaseModel):
    chat_id: int = Field(ge=10000000, le=10000000000)
    password: str
    email: EmailStr
    name: str = Field(None, max_length=15)
    last_name: str = Field(None, max_length=15)
    description: Optional[str] = Field(None, max_length=256)

class UserSign(BaseModel):
    chat_id: int = Field(ge=10000000, le=10000000000)
    password: str

class GetUser(BaseModel):
    chat_id: int = Field(ge=10000000, le=10000000000)
    registration: datetime
    last_visit: datetime
    email: EmailStr
    name: str = Field(None, max_length=15)
    last_name: str = Field(None, max_length=15)
    description: Optional[str] = Field(None, max_length=256)

class UserPatch(BaseModel):
    name: Optional[str] = Field(None, max_length=15)
    last_name: Optional[str] = Field(None, max_length=15)
    description: Optional[str] = Field(None, max_length=256)

class JWTRead(BaseModel):
    jwt: str