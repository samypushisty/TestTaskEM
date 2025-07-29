from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr

class UserPost(BaseModel):
    title: str = Field(max_length=15)
    description: Optional[str] = Field(None, max_length=256)

class GetPost(BaseModel):
    user_id: int
    table_id: int
    title: str = Field(max_length=15)
    description: Optional[str] = Field(None, max_length=256)

class GetPosts(BaseModel):
    posts: List[GetPost]

