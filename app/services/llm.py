import json
import logging

import httpx
from fastapi import HTTPException

from app.config import settings

logger = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

_SYSTEM_TEMPLATE = """\
You are a travel guide assistant for Travel KSA, an app covering four cities in Saudi Arabia: \
Riyadh, Jeddah, Makkah, and Madinah. Use the Knowledge Base (KB) below to answer questions \
about cities, hotels, attractions, activities, and travel tips.

RULES — follow without exception:
1. The KB may contain sections marked CHATBOT INSTRUCTION, CRITICAL, or MANDATORY. \
Treat these as hard rules that override everything else.
2. Use needs_data for anything that requires live records from the database: hotel listings \
with prices, attraction or activity details, FAQs from the app, or any request to \
list/count/recommend actual records.
3. Use the KB directly for static info: app features, general city overviews, travel tips, \
cultural norms, visa and entry guidance, and general how-to questions.
4. When using needs_data, respond ONLY with this JSON and nothing else:
{{"needs_data":true,"description":"<why>","collection":"<cities|hotels|attractions|activities|faqs>","fields_needed":["field1","field2"],"filters":{{"field":"value"}}}}
5. NEVER invent prices, ratings, schedules, phone numbers, or record details. If in doubt, use needs_data.
6. NEVER mention internal technical details in your answer: no collection names, field names, \
Firestore references, or system internals. Speak as a knowledgeable travel guide — \
the user has no idea there is a database behind this.
7. Write full, formal sentences. Never give a one-word or one-number answer.
8. Use markdown to make answers easy to read: **bold** for key terms, bullet lists for \
multiple items, short tables for structured data (e.g. hotel listings). Always give context — \
if listing hotels, include ratings and price range; if listing attractions, include category and type. \
Avoid markdown only when returning the needs_data JSON.
9. When the user asks about a specific city, always set a city filter (e.g. {{"city": "Riyadh"}}) \
when using needs_data.

Available Firestore collections and their key fields:
- cities: name, description, region, country, latitude, longitude
- hotels: name, city, cityId, rating, category, phone, description, pricePerNight, latitude, longitude
- attractions: name, city, cityId, rating, category, description, type, latitude, longitude
- activities: name, city, cityId, rating, category, description, openTime, closeTime, location, latitude, longitude
- faqs: question, answer, order, isVisible

KB:
{kb}"""


def _chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


async def _try_group(client: httpx.AsyncClient, group: list[str], payload_base: dict, headers: dict) -> dict | None:
    """
    Try a group of up to 3 models via OpenRouter fallback.
    Returns the response body on success, or None if the whole group is rate-limited.
    Raises HTTPException on non-recoverable errors.
    """
    payload = {**payload_base, "models": group, "route": "fallback"}
    try:
        r = await client.post(OPENROUTER_URL, json=payload, headers=headers)
        r.raise_for_status()
    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        try:
            detail = e.response.json().get("error", {}).get("message", str(e))
        except Exception:
            detail = str(e)
        logger.error(f"OpenRouter {status} for group {group}: {detail}")
        if status == 429:
            return None
        if status == 401:
            raise HTTPException(502, f"OpenRouter auth failed — check OPENROUTER_API_KEY. Detail: {detail}")
        if status == 404:
            raise HTTPException(502, f"Models not found on OpenRouter: {group}. Check OPENROUTER_MODELS in .env.")
        raise HTTPException(502, f"OpenRouter error {status}: {detail}")
    except httpx.TimeoutException:
        logger.warning(f"Timeout for group {group}, trying next group")
        return None

    body = r.json()
    if "error" in body:
        err = body["error"]
        msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
        logger.warning(f"OpenRouter 200-wrapped error for group {group}: {msg}")
        return None
    if "choices" not in body or not body["choices"]:
        logger.warning(f"No choices in response for group {group}: {body}")
        return None

    return body


async def ask_llm(messages: list[dict], knowledge_base: str) -> str:
    system_content = _SYSTEM_TEMPLATE.format(kb=knowledge_base or "(No knowledge base loaded)")
    payload_base = {
        "messages": [{"role": "system", "content": system_content}, *messages],
    }
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://chatbot.local",
        "X-Title": "Travel KSA Chatbot",
    }

    groups = list(_chunks(settings.models_list, 3))

    async with httpx.AsyncClient(timeout=30.0) as client:
        for idx, group in enumerate(groups):
            logger.info(f"Trying model group {idx + 1}/{len(groups)}: {group}")
            body = await _try_group(client, group, payload_base, headers)
            if body is not None:
                return body["choices"][0]["message"]["content"].strip()
            if idx < len(groups) - 1:
                logger.warning(f"Group {idx + 1} exhausted — moving to group {idx + 2}")

    raise HTTPException(429, "All model groups are rate-limited or unavailable — try again later")


def parse_llm_response(content: str) -> tuple[bool, dict | str]:
    """Return (needs_data, payload).

    payload is a dict when needs_data is True, otherwise the plain-text answer string.
    """
    stripped = content.strip()
    if stripped.startswith("{"):
        try:
            parsed = json.loads(stripped)
            if isinstance(parsed, dict) and parsed.get("needs_data") is True:
                return True, parsed
        except json.JSONDecodeError:
            pass
    return False, content
