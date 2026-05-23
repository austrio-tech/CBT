import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

from app.config import settings
from app.routers import chat
from app.services import firebase, knowledge

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    knowledge.load_knowledge_base(settings.kb_folder)
    logger.info(f"Knowledge base ready — {len(knowledge._sections)} sections loaded from '{settings.kb_folder}/'")
    firebase.init_firebase(settings.firebase_service_account)
    yield


app = FastAPI(
    title="Travel KSA Chatbot API",
    description="AI travel guide chatbot for Saudi Arabia with direct Firestore access.",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.method == "POST":
        raw = await request.body()
        logger.info(f">> {request.method} {request.url.path} | {raw.decode('utf-8', errors='replace')}")
        async def _receive():
            return {"type": "http.request", "body": raw}
        request._receive = _receive

    response = await call_next(request)

    chunks = []
    async for chunk in response.body_iterator:
        chunks.append(chunk)
    response_body = b"".join(chunks)
    logger.info(f"<< {request.method} {request.url.path} [{response.status_code}] | {response_body.decode('utf-8', errors='replace')}")

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )

app.include_router(chat.router)


@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok"}
