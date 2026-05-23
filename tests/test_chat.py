import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch

from app.config import settings
from app.main import app

HEADERS = {"x-api-key": settings.api_key}


@pytest.fixture(autouse=True)
def mock_firebase_init():
    """Prevent real Firebase initialization during tests."""
    with patch("app.services.firebase.init_firebase"):
        yield


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
async def test_chat_answers_directly_from_kb():
    with patch("app.services.llm.ask_llm", new=AsyncMock(return_value="Riyadh is the capital of Saudi Arabia.")):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/chat", json={"question": "Tell me about Riyadh."}, headers=HEADERS)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "answered"
    assert "Riyadh" in body["answer"]
    assert "session_id" in body


@pytest.mark.asyncio
async def test_chat_fetches_firestore_when_needed():
    """When LLM returns needs_data, chatbot queries Firestore and returns a final answer."""
    needs_data_response = '{"needs_data": true, "description": "Hotels in Jeddah", "collection": "hotels", "fields_needed": ["name", "rating", "pricePerNight"], "filters": {"city": "Jeddah"}}'
    final_answer = "Jeddah has several excellent hotels including the **Rosewood Jeddah** (rated 4.8) at SAR 1,200/night."

    firestore_data = [
        {"name": "Rosewood Jeddah", "rating": 4.8, "pricePerNight": 1200},
        {"name": "Park Hyatt Jeddah", "rating": 4.7, "pricePerNight": 950},
    ]

    with patch("app.services.llm.ask_llm", new=AsyncMock(side_effect=[needs_data_response, final_answer])), \
         patch("app.services.firebase.query_collection", new=AsyncMock(return_value=firestore_data)):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/chat", json={"question": "What hotels are in Jeddah?"}, headers=HEADERS)

    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "answered"
    assert "Jeddah" in body["answer"]


@pytest.mark.asyncio
async def test_firestore_error_returns_502():
    needs_data_response = '{"needs_data": true, "description": "Hotels in Riyadh", "collection": "hotels", "fields_needed": ["name"], "filters": {"city": "Riyadh"}}'

    with patch("app.services.llm.ask_llm", new=AsyncMock(return_value=needs_data_response)), \
         patch("app.services.firebase.query_collection", new=AsyncMock(side_effect=Exception("Firestore unavailable"))):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r = await c.post("/chat", json={"question": "List hotels in Riyadh"}, headers=HEADERS)

    assert r.status_code == 502


@pytest.mark.asyncio
async def test_conversation_history_persists():
    """session_id from first turn reuses history in the second turn."""
    with patch("app.services.llm.ask_llm", new=AsyncMock(return_value="Madinah is a holy city.")):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            r1 = await c.post("/chat", json={"question": "Tell me about Madinah."}, headers=HEADERS)
            session_id = r1.json()["session_id"]

            r2 = await c.post("/chat", json={"question": "What else?", "session_id": session_id}, headers=HEADERS)

    assert r2.status_code == 200
    assert r2.json()["session_id"] == session_id
