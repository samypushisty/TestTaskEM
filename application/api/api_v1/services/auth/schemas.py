from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


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

class UserPatch(BaseModel):
    name: Optional[str] = Field(max_length=15)
    last_name: Optional[str] = Field(max_length=15)
    description: Optional[str] = Field(None, max_length=256)

class JWTRead(BaseModel):
    jwt: str