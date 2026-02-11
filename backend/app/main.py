import uvicorn
from pathlib import Path
from fastapi import FastAPI, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from app.db import engine, Base
from app.api import otp
import requests
from fastapi.responses import HTMLResponse



app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(otp.router, prefix="/otp", tags=["otp"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")



@app.get("/secret")
def secret(authenticated: str = Cookie(None)):

    if authenticated != "true":
        return RedirectResponse(url="/")

    return RedirectResponse(
        url="https://api01-d01-rsf004br.rsf-node001.com/mba/ui/uploader-for-rs-camp/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyc2Yta2Fub2tvLXlhbmFnaSIsImV4cCI6MjU1NjExMTU5OSwiaWF0IjoxNzYyNTg2ODkzLCJqdGkiOiIxNmQ5MjgzYi0yODQzLTQ5ZTAtYjk5YS0xMDgxZjM2ZWE2MTEiLCJyb2xlIjoiYWRtaW4ifQ.unO8agZbSkpMDb2JT3OSG_d6quStrVIMzdy-tn6jcYw"
    )

# @app.get("/secret")
# def secret(authenticated: str = Cookie(None)):

#     if authenticated != "true":
#         return RedirectResponse(url="/")

#     external_url = "https://api01-d01-rsf004br.rsf-node001.com/mba/ui/uploader-for-rs-camp/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyc2Yta2Fub2tvLXlhbmFnaSIsImV4cCI6MjU1NjExMTU5OSwiaWF0IjoxNzYyNTg2ODkzLCJqdGkiOiIxNmQ5MjgzYi0yODQzLTQ5ZTAtYjk5YS0xMDgxZjM2ZWE2MTEiLCJyb2xlIjoiYWRtaW4ifQ.unO8agZbSkpMDb2JT3OSG_d6quStrVIMzdy-tn6jcYw"

#     response = requests.get(external_url)

#     return HTMLResponse(content=response.text)


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")



if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
