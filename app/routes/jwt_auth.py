from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from schemas.user import UserLoginSchema
from dtos.user import UserBaseDTO
from models.user import User
from core.jwt_utils import create_access_token, create_refresh_token, decode_token
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])

# ---------------- LOGIN ----------------
@router.post("/login")
def login(payload: UserLoginSchema):
    try:
        user = User.objects.get(username=payload.username, inactive=False, deleted_at=None)
    except User.DoesNotExist:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not pwd_context.verify(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    user_data = {"sub": str(user.id), "role": user.role}
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# ---------------- REFRESH TOKEN ----------------
@router.post("/refresh")
def refresh_token(refresh_token: str):
    decoded = decode_token(refresh_token)
    if not decoded or decoded.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_data = {"sub": decoded["sub"], "role": decoded["role"]}
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# ---------------- PROTECTED USER ----------------
def get_authenticated_user(token: str = Depends(oauth2_scheme)):
    decoded = decode_token(token)
    if not decoded or decoded.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid access token")
    try:
        user = User.objects.get(id=decoded["sub"], inactive=False, deleted_at=None)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    return UserBaseDTO(
        id=str(user.id),
        username=user.username,
        name=user.name,
        role=user.role,
        inactive=user.inactive,
        created_at=user.created_at,
        updated_at=user.updated_at,
        deleted_at=user.deleted_at
    )
