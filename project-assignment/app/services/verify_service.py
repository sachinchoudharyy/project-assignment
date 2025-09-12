from fastapi import APIRouter, HTTPException
from app.models import VerifyOTPRequest
from app.redis_client import redis_client
from app.database import users_collection
import time

router = APIRouter()

@router.post("/verify")
async def verify_otp(payload: VerifyOTPRequest):
    """
    Verify OTP for email or mobile.
    Once both are verified, move user to MongoDB.
    """
    identifier = payload.identifier
    otp = payload.otp

    # Check for email OTP
    key_email = f"otp:email:{identifier}"
    if redis_client.get(key_email) == otp:
        _mark_verified(identifier, "email_verified")
        redis_client.delete(key_email)
        return {"status": "email_verified"}

    # Check for mobile OTP
    key_mobile = f"otp:mobile:{identifier}"
    if redis_client.get(key_mobile) == otp:
        _mark_verified(identifier, "mobile_verified")
        redis_client.delete(key_mobile)
        return {"status": "mobile_verified"}

    raise HTTPException(status_code=400, detail="Invalid or expired OTP")

def _mark_verified(identifier: str, field: str):
    """
    Mark email or mobile as verified inside Redis.
    If both verified, move user to MongoDB.
    """
    for key in redis_client.keys("temp:*"):
        user = redis_client.hgetall(key)
        if user.get("email") == identifier or user.get("mobile") == identifier:
            # Mark verified field
            redis_client.hset(key, field, "true")

            
            user = redis_client.hgetall(key)
            if user.get("email_verified") == "true" and user.get("mobile_verified") == "true":
               
                users_collection.insert_one({
                    "first_name": user.get("first_name"),
                    "last_name": user.get("last_name"),
                    "email": user.get("email"),
                    "mobile": user.get("mobile"),
                    "password_hash": user.get("password_hash"),
                    "email_verified": True,
                    "mobile_verified": True,
                    "created_at": int(time.time())
                })
                # Remove temp data
                redis_client.delete(key)
