from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.birthday import router as birthday_router


app = FastAPI(
    title="Birthday Experience API",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(birthday_router)


FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

app.mount(
    "/",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend"
)


@app.get("/health")
def health():
    return {"status": "ok"}