from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db import init_db
from app.routes import auth, pages, planners, interior, session


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    Path("uploads").mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(
    title="PocketSmartAI",
    description="AI-powered personal budget and recommendation assistant",
    version="1.0.0",
    lifespan=lifespan,
)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)


# Authentication routes
app.include_router(auth.router)

# Page routes
app.include_router(pages.router)

# Planner API routes
app.include_router(planners.router)

# Interior AI route
app.include_router(interior.router)

# Session routes
app.include_router(session.router)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "app": "PocketSmartAI"
    }


@app.get("/api/health")
def api_health():
    return {
        "status": "healthy",
        "app": "PocketSmartAI"
    }