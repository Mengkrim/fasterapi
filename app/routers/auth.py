from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, validate_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db:Session = Depends(get_db)):
    # if db.query(User).filter(User.email == user.email).first():
    #     raise HTTPException(status_code=400, detail="Email already exists")
    
    validate_password(user.password)

    hashed_password = hash_password(user.password)
    
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message":"User created successfully"}

@router.post("/login")
def login(email:str, password:str, db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid crendentails")
    
    token = create_access_token({"sub":user.email})
    return {"access_token": token, "token_type": "bearer"}