from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr, model_validator

from api.v1.services.posts.schemas import GetPost


class UserReg(BaseModel):
    email: EmailStr
    password: str
    password_confirmation: Optional[str] = Field(None)
    name: str = Field(max_length=15)
    last_name: str = Field(max_length=15)
    description: Optional[str] = Field(None, max_length=256)

    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.password_confirmation:
            raise ValueError('Different passwords')
        del self.password_confirmation
        return self

class UserSign(BaseModel):
    email: EmailStr
    password: str

class UserChangePassword(BaseModel):
    old_password: str
    new_password: str
    new_password_confirmation: Optional[str] = Field(None)

    @model_validator(mode='after')
    def passwords_match(self):
        if self.new_password != self.new_password_confirmation:
            raise ValueError('Different passwords')
        del self.new_password_confirmation
        return self

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