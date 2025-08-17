from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db_url: str = "sqlite+aiosqlite:///./db.sqlite3"
    db_echo: bool = True


settings = Settings()

  