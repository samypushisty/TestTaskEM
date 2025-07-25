from datetime import datetime

from pydantic import BaseModel, Field

class UserAuth(BaseModel):
    chat_id: int = Field(ge=10000000, le=10000000000)
    password: str

class GetUser(BaseModel):
    chat_id: int = Field(ge=10000000, le=10000000000)
    registration: datetime
    last_visit: datetime

class JWTRead(BaseModel):
    jwt: str