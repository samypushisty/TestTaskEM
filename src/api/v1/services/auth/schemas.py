from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr

from api.v1.services.posts.schemas import GetPost


class UserReg(BaseModel):
    email: EmailStr
    password: str
    name: str = Field(max_length=15)
    last_name: str = Field(max_length=15)
    description: Optional[str] = Field(None, max_length=256)

class UserSign(BaseModel):
    email: EmailStr
    password: str

class GetUser(BaseModel):
    user_id: int
    registration: datetime
    last_visit: datetime
    email: EmailStr
    name: str = Field(max_length=15)
    last_name: str = Field(max_length=15)
    description: Optional[str] = Field(None, max_length=256)
    posts: List[GetPost]

class UserPatch(BaseModel):
    name: Optional[str] = Field(None, max_length=15)
    last_name: Optional[str] = Field(None, max_length=15)
    description: Optional[str] = Field(None, max_length=256)

class JWTRead(BaseModel):
    jwt: str