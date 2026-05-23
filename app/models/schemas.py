from __future__ import annotations

from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None


class AnsweredResponse(BaseModel):
    status: str = "answered"
    answer: str
    session_id: str
