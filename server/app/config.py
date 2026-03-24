from functools import lru_cache
from typing import Optional
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Database and app settings; override via environment or a `.env` file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # If set, used as the full SQLAlchemy URL (highest priority).
    database_url: Optional[str] = None

    # Composable PostgreSQL (used when `database_url` is unset). Env: POSTGRES_*.
    postgres_host: Optional[str] = None
    postgres_port: int = 5432
    postgres_user: Optional[str] = None
    postgres_password: Optional[str] = None
    postgres_db: Optional[str] = None

    # Fallback SQLite file (relative to process cwd unless absolute). Env: SQLITE_PATH.
    sqlite_path: str = "database.db"

    auth_secret_key: Optional[str] = None

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        if (
            self.postgres_host
            and self.postgres_user
            and self.postgres_password is not None
            and self.postgres_db
        ):
            u = quote_plus(self.postgres_user)
            p = quote_plus(self.postgres_password)

            return (
                f"postgresql+psycopg://{u}:{p}@{self.postgres_host}:"
                f"{self.postgres_port}/{self.postgres_db}"
            )
        return f"sqlite:///{self.sqlite_path}"

    @property
    def is_sqlite(self) -> bool:
        return self.sqlalchemy_database_url.startswith("sqlite")


@lru_cache
def get_settings() -> Settings:
    return Settings()
