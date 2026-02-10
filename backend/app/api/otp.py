from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.otp import OTP
from app.core.security import generate_otp
from datetime import datetime
from fastapi import HTTPException
from app.schemas.otp import OTPVerifyRequest
from fastapi import Response
from fastapi import Cookie

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/generate")
def create_otp(db: Session = Depends(get_db)):
    code = generate_otp()
    otp = OTP(code=code)
    db.add(otp)
    db.commit()
    db.refresh(otp)
    return {"otp": code}


@router.post("/verify")
def verify_otp(data: OTPVerifyRequest, response: Response, db: Session = Depends(get_db)):
    otp = db.query(OTP).filter(OTP.code == data.code).first()

    if not otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp.is_used:
        raise HTTPException(status_code=400, detail="OTP already used")

    if datetime.utcnow() > otp.expires_at:
        raise HTTPException(status_code=400, detail="OTP expired")

    otp.is_used = True
    db.commit()

    # 👇 認証フラグをCookieに
    response.set_cookie(key="authenticated", value="true", httponly=True)

    return {"message": "OTP verified"}


@router.get("/document")
def get_document(authenticated: str = Cookie(default=None)):
    if authenticated != "true":
        raise HTTPException(status_code=403, detail="Not authorized")

    return {"secret": "これは機密ドキュメントです"}