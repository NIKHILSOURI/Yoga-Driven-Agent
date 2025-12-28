from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import get_db, User
from typing import Optional

router = APIRouter()

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    age: int
    gender: str
    yoga_experience: str
    dietary_preferences: list
    allergies: Optional[list] = []
    goals: list
    activity_level: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    age: int
    yoga_experience: str
    
    class Config:
        from_attributes = True

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user = User(**user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.get("/user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

