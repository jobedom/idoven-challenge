# pylint: disable=redefined-outer-name, unused-argument, import-outside-toplevel

import pytest
from httpx import AsyncClient

from ..settings import (
    USER_ADMIN_EMAIL,
    USER_ADMIN_PASSWORD,
    USER_REGULAR_EMAIL,
    USER_REGULAR_PASSWORD,
    USER_UNKNOWN_EMAIL,
    USER_UNKNOWN_PASSWORD,
)


@pytest.mark.anyio
async def test_bare_login(async_client: AsyncClient) -> None:
    response = await async_client.post("/api/login")
    assert 422 == response.status_code


@pytest.mark.anyio
async def test_login_unknown(async_client: AsyncClient) -> None:
    payload = {"username": USER_UNKNOWN_EMAIL, "password": USER_UNKNOWN_PASSWORD}
    response = await async_client.post("/api/login", data=payload)
    assert 400 == response.status_code


@pytest.mark.anyio
async def test_login_admin(async_client: AsyncClient) -> None:
    payload = {"username": USER_ADMIN_EMAIL, "password": USER_ADMIN_PASSWORD}
    response = await async_client.post("/api/login", data=payload)
    assert 200 == response.status_code
    data = response.json()
    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    assert access_token is not None
    assert refresh_token is not None


@pytest.mark.anyio
async def test_login_regular(async_client: AsyncClient, admin_access_token: str) -> None:
    headers = {"Authorization": f"Bearer {admin_access_token}"}
    payload = {"email": USER_REGULAR_EMAIL, "password": USER_REGULAR_PASSWORD, "is_admin": False}
    response = await async_client.post("/api/user", headers=headers, json=payload)

    payload = {"username": USER_REGULAR_EMAIL, "password": USER_REGULAR_PASSWORD}
    response = await async_client.post("/api/login", data=payload)
    assert 200 == response.status_code
    data = response.json()
    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    assert access_token is not None
    assert refresh_token is not None


@pytest.mark.anyio
async def test_no_token_create_user(async_client: AsyncClient) -> None:
    payload = {"email": USER_REGULAR_EMAIL, "password": USER_REGULAR_PASSWORD, "is_admin": False}
    response = await async_client.post("/api/user", json=payload)
    assert 401 == response.status_code


@pytest.mark.anyio
async def test_regular_create_user(async_client: AsyncClient, regular_access_token: str) -> None:
    headers = {"Authorization": f"Bearer {regular_access_token}"}
    payload = {"email": USER_REGULAR_EMAIL, "password": USER_REGULAR_PASSWORD, "is_admin": False}
    response = await async_client.post("/api/user", headers=headers, json=payload)
    assert 403 == response.status_code


@pytest.mark.anyio
async def test_avoid_duplicated_create_user(async_client: AsyncClient, admin_access_token: str) -> None:
    headers = {"Authorization": f"Bearer {admin_access_token}"}
    payload = {"email": USER_REGULAR_EMAIL, "password": USER_REGULAR_PASSWORD, "is_admin": False}
    response = await async_client.post("/api/user", headers=headers, json=payload)
    assert 400 == response.status_code  # Existing user


@pytest.mark.anyio
async def test_admin_get_all_users(async_client: AsyncClient, admin_access_token: str) -> None:
    headers = {"Authorization": f"Bearer {admin_access_token}"}
    response = await async_client.get("/api/user", headers=headers)
    assert 200 == response.status_code
    data = response.json()
    assert data.get("users") is not None


@pytest.mark.anyio
async def test_regular_get_all_users(async_client: AsyncClient, regular_access_token: str) -> None:
    headers = {"Authorization": f"Bearer {regular_access_token}"}
    response = await async_client.get("/api/user", headers=headers)
    assert 403 == response.status_code


@pytest.mark.anyio
async def test_admin_get_user(async_client: AsyncClient, admin_access_token: str) -> None:
    headers = {"Authorization": f"Bearer {admin_access_token}"}
    payload = {"email": USER_REGULAR_EMAIL, "password": USER_REGULAR_PASSWORD, "is_admin": False}
    await async_client.post("/api/user", headers=headers, json=payload)

    response = await async_client.get("/api/user", headers=headers)
    data = response.json()
    for user in data["users"]:
        user_id = user["id"]
        response = await async_client.get(f"/api/user/{user_id}", headers=headers)
        assert 200 == response.status_code
