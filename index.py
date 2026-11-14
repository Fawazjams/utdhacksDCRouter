"""Vercel entrypoint: serves the same FastAPI app (API + frontend) as `uvicorn app.main:app` in backend/."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "backend"))

from app.main import app  # noqa: E402,F401
