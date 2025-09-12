from fastapi import APIRouter, HTTPException
from app.models import SignupRequest
from app.utils import generate_otp, hash_password
from app.redis_client import redis_client
import uuid
import os

router = APIRouter()


OTP_TTL = int(os.getenv("OTP_TTL", 300))       # 5 minutes
TEMP_TTL = int(os.getenv("TEMP_TTL", 86400))   # 24 hours

@router.post("/signup")
def signup(payload: SignupRequest):
    """
    Signup API:
    - Accepts user details
    - Stores them in Redis (temporary)
    - Generates OTPs for email & mobile
    """

    # Create unique temporary ID
    temp_id = str(uuid.uuid4())

   
    password_hash = hash_password(payload.password)

    
    redis_client.hset(f"temp:{temp_id}", mapping={
        "first_name": payload.first_name,
        "last_name": payload.last_name or "",
        "email": payload.email,
        "mobile": payload.mobile,
        "password_hash": password_hash,
        "email_verified": "false",
        "mobile_verified": "false"
    })
    redis_client.expire(f"temp:{temp_id}", TEMP_TTL)

    
    otp_email = generate_otp()
    otp_mobile = generate_otp()

    # Save OTPs with expiry
    redis_client.setex(f"otp:email:{payload.email}", OTP_TTL, otp_email)
    redis_client.setex(f"otp:mobile:{payload.mobile}", OTP_TTL, otp_mobile)

    
    return {
        "status": "pending_verification",
        "temp_id": temp_id,
        "otp_email": otp_email,
        "otp_mobile": otp_mobile
    }
