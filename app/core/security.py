from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

# =====================
# Password hashing
# =====================

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def validate_password(password: str):
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password must be 72 bytes or less")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# =====================
# JWT
# =====================

SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
