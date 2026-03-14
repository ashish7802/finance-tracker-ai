from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    database_url: str
    jwt_secret: str
    anthropic_api_key: str | None
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24

    def __init__(self) -> None:
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./finance.db")
        self.jwt_secret = os.getenv("JWT_SECRET", "dev-secret-change-me")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")


@lru_cache
def get_settings() -> Settings:
    return Settings()
