
from fastapi import FastAPI
from app.services import signup_service, verify_service

app = FastAPI(title="Signup & OTP Verification API")


app.include_router(signup_service.router, prefix="/auth", tags=["Signup"])
app.include_router(verify_service.router, prefix="/auth", tags=["Verify"])

@app.get("/")
def root():
    return {"message": "API is running"}

