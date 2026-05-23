import asyncio
import logging
from typing import Any

import firebase_admin
from firebase_admin import credentials, firestore

logger = logging.getLogger(__name__)

_db = None


def init_firebase(service_account_path: str) -> None:
    global _db
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)
    _db = firestore.client()
    logger.info("Firebase Admin SDK initialized")


async def query_collection(
    collection: str,
    filters: dict[str, Any],
    fields_needed: list[str],
) -> list[dict[str, Any]]:
    """Query a Firestore collection with equality filters, returning only requested fields."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _query_sync, collection, filters, fields_needed)


def _query_sync(
    collection: str,
    filters: dict[str, Any],
    fields_needed: list[str],
) -> list[dict[str, Any]]:
    ref = _db.collection(collection)
    for field, value in filters.items():
        ref = ref.where(filter=firestore.FieldFilter(field, "==", value))
    docs = ref.get()
    results = []
    for doc in docs:
        data = doc.to_dict() or {}
        if fields_needed:
            data = {f: data[f] for f in fields_needed if f in data}
        results.append(data)
    logger.info(f"Firestore query: collection={collection} filters={filters} → {len(results)} docs")
    return results
