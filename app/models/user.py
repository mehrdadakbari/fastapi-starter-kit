from mongoengine import Document, StringField, DateTimeField, BooleanField, EnumField
from datetime import datetime
from enum import Enum
from passlib.context import CryptContext
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(Document):
    # MongoDB automatically provides _id, we can alias it as id
    id = StringField(primary_key=True, default=lambda: str(ObjectId()))

    username = StringField(max_length=32, required=True, unique=True)
    password = StringField(max_length=128, required=True)
    inactive = BooleanField(default=False)

    name = StringField(max_length=64, required=True)
    role = EnumField(UserRole, default=UserRole.USER)

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    deleted_at = DateTimeField(default=None, null=True)

    meta = {
        "collection": "users",
        "indexes": [
            {"fields": ["username"], "unique": True}
        ],
        "ordering": ["-created_at"]
    }

    # -----------------------------
    # Password management
    # -----------------------------
    def set_password(self, password: str):
        """Hash and store the password."""
        self.password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify provided password against hashed password."""
        return pwd_context.verify(password, self.password)

    # -----------------------------
    # Soft delete helper
    # -----------------------------
    def soft_delete(self):
        """Mark the document as deleted."""
        self.deleted_at = datetime.utcnow()
        self.save()
