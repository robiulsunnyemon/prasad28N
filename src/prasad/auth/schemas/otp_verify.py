from pydantic import BaseModel,EmailStr


class UserOTPVerify(BaseModel):
    email: EmailStr
    otp: str