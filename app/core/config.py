from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    app_name: str = "FastAPI Starter Kit"
    version: str = "0.1.0"
    debug: bool = True
    environment: str = "development"  # development | production | staging

    # Database (MongoDB)
    db_user: str = "starter_kit"
    db_password: str = "starter_kit"
    db_host: str = "localhost"
    db_port: int = 27017
    db_name: str = "fastapi_starter"
    mongo_uri: str = "mongodb://starter_kit:starter_kit@localhost:27017/fastapi_starter"

    # Security / JWT
    secret_key: str = 'secret_key'
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30

    # CORS
    cors_origins: List[str] = ["*"]


    @property
    def db_url(self) -> str:
        if self.mongo_uri:
            return self.mongo_uri
        return (
            f"mongodb://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


# Create global settings instance
settings = Settings()
