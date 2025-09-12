from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):# this is for signup request
    first_name: str
    last_name: str | None = None
    email: EmailStr
    mobile: str
    password: str


class VerifyOTPRequest(BaseModel):# and this is for OTP verification request
    identifier: str   # can be email or mobile
    otp: str
