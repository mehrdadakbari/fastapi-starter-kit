from pydantic import BaseModel, Field, field_validator
from typing import Optional
from passlib.context import CryptContext
from dtos.user import UserRole
from dtos.user import UserBaseDTO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------------------
# Input Schemas
# -----------------------------
class UserCreateSchema(BaseModel):
    username: str = Field(..., max_length=32)
    name: str = Field(..., max_length=64)
    password: str = Field(..., max_length=256)
    role: UserRole = Field(default=UserRole.USER)
    inactive: bool = Field(default=False)

    @field_validator("password", mode="before")
    @classmethod
    def hash_password(cls, v: str) -> str:
        """Automatically hash the password before saving."""
        return pwd_context.hash(v)


class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=64)
    password: Optional[str] = Field(None, max_length=256)
    inactive: Optional[bool] = None
    role: Optional[UserRole] = None

    @field_validator("password", mode="before")
    def hash_password(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return pwd_context.hash(v)
        return v


class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=32)
    password: str = Field(..., max_length=256)


class UserRefreshTokenSchema(BaseModel):
    token: str = Field(..., max_length=512)


# -----------------------------
# Output Schema
# -----------------------------
class UserResponseSchema(UserBaseDTO):
    pass