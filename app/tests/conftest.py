# pylint: disable=redefined-outer-name, unused-argument, import-outside-toplevel

import os
import warnings
from typing import AsyncGenerator  # , Generator

import alembic
import pytest
from alembic.config import Config
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from .settings import USER_ADMIN_EMAIL, USER_ADMIN_PASSWORD, USER_REGULAR_EMAIL, USER_REGULAR_PASSWORD

# from app.db import get_session

# from sqlalchemy import create_engine, event, text
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
# from sqlalchemy.orm import Session, SessionTransaction

# from app.models.base import Base
# from app.settings import settings


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def with_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["APP_CONFIG_FILE"] = "test"
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", "sqlite+aiosqlite:///db/test-database.db")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture
def app(with_migrations: None) -> FastAPI:
    from app.main import app

    return app


@pytest.fixture
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
async def admin_access_token(async_client: AsyncClient) -> AsyncGenerator:
    payload = {"username": USER_ADMIN_EMAIL, "password": USER_ADMIN_PASSWORD}
    response = await async_client.post("/api/login", data=payload)
    yield response.json().get("access_token")


@pytest.fixture
async def regular_access_token(async_client: AsyncClient, admin_access_token: str) -> AsyncGenerator:
    payload = {"username": USER_REGULAR_EMAIL, "password": USER_REGULAR_PASSWORD}
    response = await async_client.post("/api/login", data=payload)
    yield response.json().get("access_token")


# @pytest.fixture(scope="session")
# def setup_db() -> Generator:
#     engine = create_engine(f"{settings.DB_URI.replace('+aiosqlite', '')}")
#     conn = engine.connect()
#     # conn.execute(text("commit"))
#     try:
#         conn.execute(text("drop database test"))
#     except SQLAlchemyError:
#         pass
#     finally:
#         conn.close()
#     conn = engine.connect()
#     # conn.execute(text("commit"))
#     conn.execute(text("create database test"))
#     conn.close()
#     yield
#     conn = engine.connect()
#     # conn.execute(text("commit"))
#     try:
#         conn.execute(text("drop database test"))
#     except SQLAlchemyError:
#         pass
#     conn.close()
#     engine.dispose()


# @pytest.fixture(scope="session", autouse=True)
# def setup_test_db(setup_db: Generator) -> Generator:
#     engine = create_engine(f"{settings.DB_URI.replace('+aiosqlite', '')}/test")
#     with engine.begin():
#         Base.metadata.drop_all(engine)
#         Base.metadata.create_all(engine)
#         yield
#         Base.metadata.drop_all(engine)
#     engine.dispose()


# @pytest.fixture
# async def session() -> AsyncGenerator:
#     async_engine = create_async_engine(f"{settings.DB_URI}")
#     async with async_engine.connect() as conn:
#         await conn.begin()
#         await conn.begin_nested()
#         async_session_local_class = async_sessionmaker(
#             autocommit=False,
#             autoflush=False,
#             bind=conn,
#             future=True,
#         )
#         async_session = async_session_local_class()

#         @event.listens_for(async_session.sync_session, "after_transaction_end")
#         def end_savepoint(session: Session, transaction: SessionTransaction) -> None:
#             if conn.closed:
#                 return
#             if not conn.in_nested_transaction():
#                 if conn.sync_connection:
#                     conn.sync_connection.begin_nested()

#         def test_get_session() -> Generator:
#             try:
#                 yield async_session_local_class
#             except SQLAlchemyError:
#                 pass

#         app.dependency_overrides[get_session] = test_get_session
#         yield async_session
#         await async_session.close()
#         await conn.rollback()
#     await async_engine.dispose()
