from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 🔒 rename to avoid shadowing
password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def validate_password(password: str):
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password too long (max 72 bytes)")

def hash_password(password: str):
    validate_password(password)
    return password_context.hash(password.strip())

def verify_password(password: str, hashed: str):
    validate_password(password)
    return password_context.verify(password.strip(), hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
