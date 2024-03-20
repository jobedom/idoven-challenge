from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def async_client() -> AsyncGenerator:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="https://test") as client:
        yield client
