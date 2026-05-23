import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch

from app.config import settings
from app.main import app

HEADERS = {"x-api-key": settings.api_key}


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_missing_api_key_is_rejected():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/chat", json={"question": "What hotels are in Riyadh?"})
    assert r.status_code in (403, 422)


@pytest.mark.asyncio
async def test_wrong_api_key_is_rejected():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/chat", json={"question": "What hotels are in Riyadh?"}, headers={"x-api-key": "wrong"})
    assert r.status_code == 403


@pytest.mark.asyncio
async def test_chat_returns_direct_answer():
    with patch("app.services.llm.ask_llm", new=AsyncMock(return_value="Riyadh is the capital of Saudi Arabia.")):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/chat", json={"question": "Tell me about Riyadh."}, headers=HEADERS)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "answered"
    assert "Riyadh" in body["answer"]


@pytest.mark.asyncio
async def test_chat_returns_data_needed():
    mock_json = '{"needs_data": true, "description": "Hotels in Jeddah", "collection": "hotels", "fields_needed": ["name", "rating", "pricePerNight"], "filters": {"city": "Jeddah"}}'
    with patch("app.services.llm.ask_llm", new=AsyncMock(return_value=mock_json)):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/chat", json={"question": "What hotels are in Jeddah?"}, headers=HEADERS)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "data_needed"
    assert "ref_code" in body
    assert body["data_request"]["collection"] == "hotels"
    assert body["data_request"]["filters"] == {"city": "Jeddah"}


@pytest.mark.asyncio
async def test_respond_with_unknown_ref_code_returns_404():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        r = await c.post("/chat/respond", json={"ref_code": "does-not-exist", "data": {}}, headers=HEADERS)
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_full_two_phase_flow():
    """Phase 1 returns data_needed; phase 2 with Firestore data returns the final answer."""
    data_needed_mock = '{"needs_data": true, "description": "Attractions in Makkah", "collection": "attractions", "fields_needed": ["name", "rating", "type", "description"], "filters": {"city": "Makkah"}}'
    final_answer_mock = "Makkah is home to the **Grand Mosque (Al-Masjid Al-Haram)**, the holiest site in Islam."

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        # Phase 1
        with patch("app.services.llm.ask_llm", new=AsyncMock(return_value=data_needed_mock)):
            r1 = await c.post("/chat", json={"question": "What are the top attractions in Makkah?"}, headers=HEADERS)
        assert r1.status_code == 200
        assert r1.json()["status"] == "data_needed"
        ref_code = r1.json()["ref_code"]

        # Phase 2
        with patch("app.services.llm.ask_llm", new=AsyncMock(return_value=final_answer_mock)):
            r2 = await c.post(
                "/chat/respond",
                json={
                    "ref_code": ref_code,
                    "data": [
                        {"name": "Al-Masjid Al-Haram", "rating": 5.0, "type": "religious", "description": "The Grand Mosque"},
                    ],
                },
                headers=HEADERS,
            )
        assert r2.status_code == 200
        assert r2.json()["status"] == "answered"
        assert "Makkah" in r2.json()["answer"]


@pytest.mark.asyncio
async def test_ref_code_consumed_after_respond():
    """A ref_code cannot be reused after a successful /respond."""
    data_needed_mock = '{"needs_data": true, "description": "test", "collection": "hotels", "fields_needed": ["name"]}'
    final_answer_mock = "Done."

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        with patch("app.services.llm.ask_llm", new=AsyncMock(return_value=data_needed_mock)):
            r1 = await c.post("/chat", json={"question": "test question"}, headers=HEADERS)
        ref_code = r1.json()["ref_code"]

        with patch("app.services.llm.ask_llm", new=AsyncMock(return_value=final_answer_mock)):
            await c.post("/chat/respond", json={"ref_code": ref_code, "data": [{"name": "test"}]}, headers=HEADERS)

        r3 = await c.post("/chat/respond", json={"ref_code": ref_code, "data": [{"name": "test"}]}, headers=HEADERS)
    assert r3.status_code == 404
