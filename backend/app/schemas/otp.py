from pydantic import BaseModel

class OTPVerifyRequest(BaseModel):
    code: str
