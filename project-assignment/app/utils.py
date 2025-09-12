import secrets
from passlib.context import CryptContext

# Configure bcrypt for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_otp(length: int = 6) -> str:
    """
    Generate a numeric OTP of given length (default 6 digits).
    """
    return ''.join(secrets.choice("0123456789") for _ in range(length))

def hash_password(password: str) -> str:
    """
    Hash a plain password using bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a plain password against a bcrypt hash.
    """
    return pwd_context.verify(password, hashed)
