# pylint: disable=redefined-outer-name, unused-argument, import-outside-toplevel, global-statement

from datetime import datetime, timezone

import pytest
from httpx import AsyncClient

NEW_ECG_PAYLOAD = {
    "id": "ecg_1",
    "owner_id": None,
    "date": datetime.now(timezone.utc).isoformat(),
    "leads": [
        {"name": "aVR", "signal": [1, -2, 3, -4, 5], "sample_count": 5},
        {"name": "aVL", "signal": [1, -2, 3, -4, 5, 6, 7, -8]},
    ],
}

CORRECT_INSIGHTS_ZERO_CROSSINGS = {
    "aVR": 4,
    "aVL": 5,
}

CREATED_ECG_ID = None


@pytest.mark.anyio
async def test_create_ecg_admin_user(async_client: AsyncClient, admin_access_token: str) -> None:
    headers = {"Authorization": f"Bearer {admin_access_token}"}
    payload = NEW_ECG_PAYLOAD.copy()
    payload["owner_id"] = 1  # Admin user
    response = await async_client.post("/api/ecg", headers=headers, json=payload)
    assert 403 == response.status_code


@pytest.mark.anyio
async def test_create_ecg_regular_user(async_client: AsyncClient, regular_access_token: str) -> None:
    global CREATED_ECG_ID
    headers = {"Authorization": f"Bearer {regular_access_token}"}
    payload = NEW_ECG_PAYLOAD.copy()
    payload["owner_id"] = 2  # Regular user
    response = await async_client.post("/api/ecg", headers=headers, json=payload)
    assert 200 == response.status_code
    data = response.json()
    CREATED_ECG_ID = data["id"]


@pytest.mark.anyio
async def test_get_ecg_admin_user(async_client: AsyncClient, admin_access_token: str) -> None:
    headers = {"Authorization": f"Bearer {admin_access_token}"}
    response = await async_client.get(f"/api/ecg/{CREATED_ECG_ID}", headers=headers)
    assert 403 == response.status_code


@pytest.mark.anyio
async def test_get_ecg_regular_user(async_client: AsyncClient, regular_access_token: str) -> None:
    headers = {"Authorization": f"Bearer {regular_access_token}"}
    response = await async_client.get(f"/api/ecg/{CREATED_ECG_ID}", headers=headers)
    assert 200 == response.status_code


@pytest.mark.anyio
async def test_delete_ecg_admin_user(async_client: AsyncClient, admin_access_token: str) -> None:
    headers = {"Authorization": f"Bearer {admin_access_token}"}
    response = await async_client.delete(f"/api/ecg/{CREATED_ECG_ID}", headers=headers)
    assert 403 == response.status_code


@pytest.mark.anyio
async def test_delete_ecg_regular_user(async_client: AsyncClient, regular_access_token: str) -> None:
    headers = {"Authorization": f"Bearer {regular_access_token}"}
    response = await async_client.get(f"/api/ecg/{CREATED_ECG_ID}", headers=headers)
    assert 200 == response.status_code


@pytest.mark.anyio
async def test_get_insights_admin_user(async_client: AsyncClient, admin_access_token: str) -> None:
    headers = {"Authorization": f"Bearer {admin_access_token}"}
    response = await async_client.get(f"/api/insights/{CREATED_ECG_ID}", headers=headers)
    assert 403 == response.status_code


@pytest.mark.anyio
async def test_get_insights_regular_user(async_client: AsyncClient, regular_access_token: str) -> None:
    headers = {"Authorization": f"Bearer {regular_access_token}"}
    response = await async_client.get(f"/api/insights/{CREATED_ECG_ID}", headers=headers)
    assert 200 == response.status_code
    data = response.json()
    assert data.get("ecg_insights") is not None
    insights = data["ecg_insights"]
    for insight in insights:
        lead = insight["lead"]
        zero_crossings = insight["insights"][0]["zero_crossings"]
        assert CORRECT_INSIGHTS_ZERO_CROSSINGS.get(lead) is not None
        assert CORRECT_INSIGHTS_ZERO_CROSSINGS[lead] == zero_crossings
