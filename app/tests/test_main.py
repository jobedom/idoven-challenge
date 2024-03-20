import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_health(async_client: AsyncClient) -> None:
    response = await async_client.get("/")
    assert 200 == response.status_code
