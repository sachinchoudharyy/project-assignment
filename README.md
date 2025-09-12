# Signup & OTP Verification (FastAPI + Redis + MongoDB)

## Overview
This project implements a "user signup and OTP verification system":
- FastAPI → Backend framework
- Redis → Temporary storage (user data + OTPs)
- MongoDB → Permanent storage (after verification)

Flow:
1. User signs up → Data saved in Redis + OTPs generated
2. User verifies mobile & email via OTP
3. Once both are verified → User is moved into MongoDB


