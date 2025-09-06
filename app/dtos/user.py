from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic_core import core_schema
from bson import ObjectId

class PyObjectId(ObjectId):
    """Custom type for MongoDB ObjectId as string"""
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, v, info=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserBaseDTO(BaseModel):
    id: PyObjectId = Field(...)
    username: str = Field(..., max_length=32)
    name: str = Field(..., max_length=64)
    role: UserRole = Field(default=UserRole.USER)
    inactive: bool = Field(default=False)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
