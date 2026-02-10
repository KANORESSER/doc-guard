from fastapi import FastAPI
from app.db import engine, Base
from app.models import otp  # モデル読み込み
from app.api import otp
from fastapi.staticfiles import StaticFiles
import uvicorn
from pathlib import Path

app = FastAPI()
app.include_router(otp.router, prefix="/otp", tags=["otp"])

Base.metadata.create_all(bind=engine)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
