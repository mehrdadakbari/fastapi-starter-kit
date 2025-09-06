# app/routers/user.py
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from models.user import User
from schemas.user import (
    UserCreateSchema,
    UserUpdateSchema,
)
from dtos.user import UserBaseDTO
from mongoengine.errors import NotUniqueError, DoesNotExist, ValidationError
from core.logging_config import setup_logging
import logging
from datetime import datetime, timezone

setup_logging()
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserBaseDTO, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreateSchema):
    """Create a new user."""
    try:
        user = User(**payload.model_dump())
        user.save()
        logger.success(f"✅ Created user {user.username}")
        user_data = user.to_mongo().to_dict()
        user_data["id"] = str(user_data.pop("_id"))
        return UserBaseDTO.model_validate(user_data)
    except NotUniqueError:
        logger.warning(f"⚠️ Username {payload.username} already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )
    except ValidationError as e:
        logger.error(f"❌ Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.get("/", response_model=List[UserBaseDTO])
def get_users():
    """Get all active users."""
    return [
        UserBaseDTO.model_validate({**u.to_mongo().to_dict(), "id": str(u.id)})
        for u in User.objects(deleted_at=None)
    ]

@router.get("/{user_id}", response_model=UserBaseDTO)
def get_user(user_id: str):
    """Get an active user by ID."""
    try:
        user = User.objects.get(id=user_id, inactive=False, deleted_at=None)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    # Convert MongoEngine document to dict and include string ID
    user_dict = {**user.to_mongo().to_dict(), "id": str(user.id)}
    return UserBaseDTO.model_validate(user_dict)


@router.put("/{user_id}", response_model=UserBaseDTO)
def update_user(user_id: str, payload: UserUpdateSchema):
    """Update an active user."""
    try:
        user = User.objects.get(id=user_id, inactive=False, deleted_at=None)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    # Apply only the fields provided in the payload
    update_data = payload.model_dump(exclude_unset=True)
    if update_data:
        user.update(**update_data)
        user.reload()
        logger.success(f"🔄 Updated user {user.username}")

    # Convert to dict and include string ID
    user_dict = {**user.to_mongo().to_dict(), "id": str(user.id)}
    return UserBaseDTO.model_validate(user_dict)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    """Soft delete a user (mark as deleted)."""
    try:
        user = User.objects.get(id=user_id, inactive=False, deleted_at=None)
        user.update(set__deleted_at=datetime.now(timezone.utc), set__inactive=True)
        logger.success(f"🗑️ Deleted user {user.username}")
        return None
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
