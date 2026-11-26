"""FastAPI entrypoint for KTU Activity Points Checker backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.activities import router as activities_router
from app.api.dashboard import router as dashboard_router
from app.api.export import router as export_router
from app.api.profile import router as profile_router
from app.api.rules import router as rules_router

app = FastAPI(
    title="KTU Activity Points Checker API",
    description="Deterministic rules engine and verification API for KTU 2024 Scheme Activity Points.",
    version="1.0.0",
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(profile_router)
app.include_router(rules_router)
app.include_router(activities_router)
app.include_router(dashboard_router)
app.include_router(export_router)


@app.get("/api/health", tags=["system"])
def healthcheck() -> dict[str, str]:
    """Basic healthcheck endpoint."""
    return {"status": "ok", "scheme": "2024", "version": "1.0.0"}
