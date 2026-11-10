from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.database import PatientDB
from app.routes import router

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_FILE = PROJECT_ROOT / "data" / "patients.json"


def create_app(database_path: str | Path = DEFAULT_DATA_FILE) -> FastAPI:
    @asynccontextmanager
    async def lifespan(api: FastAPI) -> AsyncIterator[None]:
        api.state.db = PatientDB(database_path)
        yield

    api = FastAPI(
        title="Patient Management System API",
        lifespan=lifespan,
    )
    api.include_router(router)
    return api


app = create_app()
