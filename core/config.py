from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "db.sqlite3"


class DbSettings(BaseModel):
    url: str = "sqlite+aiosqlite:///./db.sqlite3"
    echo: bool = True


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()

settings = Settings()

  