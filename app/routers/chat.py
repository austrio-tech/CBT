import json
import logging

from fastapi import APIRouter, Depends, Header, HTTPException

from app.config import settings
from app.models.schemas import AnsweredResponse, ChatRequest
from app.services import firebase, knowledge, llm
from app.services import session as session_store

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["Chat"])


async def require_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")


@router.post("", response_model=AnsweredResponse)
async def chat(req: ChatRequest, _=Depends(require_api_key)):
    session_id, history = session_store.get_or_create_conversation(
        req.session_id, settings.session_ttl_minutes
    )

    kb = knowledge.get_relevant_kb(req.question)
    messages = [*history, {"role": "user", "content": req.question}]

    raw = await llm.ask_llm(messages, kb)
    needs_data, payload = llm.parse_llm_response(raw)

    if needs_data:
        assert isinstance(payload, dict)
        try:
            data = await firebase.query_collection(
                collection=payload.get("collection", ""),
                filters=payload.get("filters", {}),
                fields_needed=payload.get("fields_needed", []),
            )
        except Exception as e:
            logger.error(f"Firestore query failed: {e}")
            raise HTTPException(502, "Failed to fetch data from the database")

        followup = [{
            "role": "user",
            "content": (
                f"Question: {req.question}\n\n"
                f"Data from the database:\n{json.dumps(data, ensure_ascii=False, separators=(',', ':'))}\n\n"
                f"Answer the question using this data. Write a full, formal response with markdown formatting."
            ),
        }]
        raw = await llm.ask_llm(followup, kb)
        _, payload = llm.parse_llm_response(raw)

    answer = str(payload)
    session_store.append_turn(
        session_id, req.question, answer,
        max_turns=settings.conversation_max_turns,
        ttl_minutes=settings.session_ttl_minutes,
    )
    return AnsweredResponse(answer=answer, session_id=session_id)
