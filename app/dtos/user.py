from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserBaseDTO(BaseModel):
    id: Optional[str] = None
    username: str = Field(..., max_length=32)
    name: str = Field(..., max_length=64)
    role: UserRole = Field(default=UserRole.USER)
    inactive: bool = Field(default=False)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
