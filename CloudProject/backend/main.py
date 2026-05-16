from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.db.session import engine
from backend.db.init_db import init_db
from backend.api.routes import migrations, janitor, health, logs


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialise DB tables
    init_db()
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title="Cloud Janitor API",
    description="Backend API for DB migration management and cloud resource cleanup.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(migrations.router, prefix="/migrations", tags=["Migrations"])
app.include_router(janitor.router, prefix="/janitor", tags=["Janitor"])
app.include_router(logs.router, prefix="/logs", tags=["Logs"])
