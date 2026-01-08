from fastapi import APIRouter,Depends
from app.dependencies import get_current_user, get_db
# from sqlalchemy.orm import Session
# from app.database import SessionLocal
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

# def get_db():
#     db=SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user