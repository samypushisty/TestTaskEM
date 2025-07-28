from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr

class PermissionShem(BaseModel):
    permission_id: int
    name: str
    description: str

class GetUser(BaseModel):
    user_id: int
    registration: datetime
    last_visit: datetime
    email: EmailStr
    name: str = Field(None, max_length=15)
    last_name: str = Field(None, max_length=15)
    description: Optional[str] = Field(None, max_length=256)
    permissions: List[PermissionShem]
