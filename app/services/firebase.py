import asyncio
import json
import logging
import os
from typing import Any

import firebase_admin
from firebase_admin import credentials, firestore

logger = logging.getLogger(__name__)

_db = None


def init_firebase(service_account_path: str) -> None:
    """Initialize Firebase Admin SDK.

    On cloud deployments (e.g. Render) where file upload is not possible,
    set the FIREBASE_SERVICE_ACCOUNT_JSON env var to the full JSON content
    of the service account key. Locally, place the JSON file at
    service_account_path and leave FIREBASE_SERVICE_ACCOUNT_JSON unset.
    """
    global _db
    json_str = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")
    if json_str:
        cred = credentials.Certificate(json.loads(json_str))
        logger.info("Firebase: loading credentials from FIREBASE_SERVICE_ACCOUNT_JSON env var")
    elif os.path.exists(service_account_path):
        cred = credentials.Certificate(service_account_path)
        logger.info(f"Firebase: loading credentials from file '{service_account_path}'")
    else:
        raise RuntimeError(
            "Firebase credentials not found. "
            "On Render/cloud: set the FIREBASE_SERVICE_ACCOUNT_JSON environment variable "
            "to the full contents of your service account JSON. "
            "Locally: place service-account.json in the project root."
        )
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
