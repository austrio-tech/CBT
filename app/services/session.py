import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class Conversation:
    history: list[dict] = field(default_factory=list)
    expires_at: datetime = field(default_factory=datetime.utcnow)


_conversations: dict[str, Conversation] = {}


def get_or_create_conversation(
    session_id: Optional[str],
    ttl_minutes: int = 30,
) -> tuple[str, list[dict]]:
    """Return (session_id, history_so_far). Creates a new conversation if needed."""
    if session_id:
        conv = _conversations.get(session_id)
        if conv and datetime.utcnow() <= conv.expires_at:
            conv.expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)
            return session_id, list(conv.history)

    new_id = str(uuid.uuid4())
    _conversations[new_id] = Conversation(
        expires_at=datetime.utcnow() + timedelta(minutes=ttl_minutes)
    )
    return new_id, []


def append_turn(
    session_id: str,
    question: str,
    answer: str,
    max_turns: int = 3,
    ttl_minutes: int = 30,
) -> None:
    """Add a completed Q&A turn to the conversation, capped at max_turns pairs."""
    conv = _conversations.get(session_id)
    if conv is None:
        return
    conv.history.append({"role": "user", "content": question})
    conv.history.append({"role": "assistant", "content": answer})
    if len(conv.history) > max_turns * 2:
        conv.history = conv.history[-(max_turns * 2):]
    conv.expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)
