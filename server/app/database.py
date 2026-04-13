from typing import Annotated

from fastapi import Depends
from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings

_settings = get_settings()
_url = _settings.sqlalchemy_database_url
_engine_kwargs: dict = {}
if _settings.is_sqlite:
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    _engine_kwargs["pool_pre_ping"] = True

engine = create_engine(_url, **_engine_kwargs)


def _reset_schema() -> None:
    """Drop mapped tables. PostgreSQL uses CASCADE so stray FKs (e.g. old columns) do not block drops."""
    from app.models import Book, BookAuthorLink, User, UserBookLink, Author  # noqa: F401 — register metadata

    if _settings.is_sqlite:
        SQLModel.metadata.drop_all(engine)
        return

    tables = list(reversed(SQLModel.metadata.sorted_tables))
    with engine.begin() as conn:
        preparer = conn.dialect.identifier_preparer
        for table in tables:
            conn.execute(
                text(f"DROP TABLE IF EXISTS {preparer.format_table(table)} CASCADE")
            )


def create_db_and_tables() -> None:
    # Import models so table metadata is registered before create_all.
    from app.models import User, Book, Author, UserBookLink, BookAuthorLink  # noqa: F401

    if _settings.reset_database_on_startup:
        _reset_schema()
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]