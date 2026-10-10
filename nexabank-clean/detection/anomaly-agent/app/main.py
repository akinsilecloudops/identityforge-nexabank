
import secrets
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

from app import config, db
from app.pipeline import load_baseline, process_event
from app.schemas import Event


if config.SENTRY_DSN:
    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        environment=config.ENVIRONMENT,
        traces_sample_rate=0.0,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init()
    yield


app = FastAPI(
    title="NexaBank Anomaly Agent",
    version="1.0.0",
    lifespan=lifespan,
)


def require_api_key(x_api_key: str = Header(default="")):
    expected = config.INGEST_API_KEY

    if not expected or not secrets.compare_digest(x_api_key, expected):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
        )


@app.get("/health")
def health():
    return {
        "status": "ok",
        "baseline_agents": len(load_baseline()),
    }


@app.get("/stats")
def get_stats():
    return db.stats()


@app.post("/events", dependencies=[Depends(require_api_key)])
def ingest_event(event: Event):
    try:
        return process_event(event.model_dump(mode="json"))
    except Exception as exc:
        sentry_sdk.capture_exception(exc)
        raise HTTPException(
            status_code=500,
            detail="Event processing failed",
        ) from exc


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )
