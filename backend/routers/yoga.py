from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, YogaPlan, User
from agents.yoga_agent import YogaAgent
from typing import Optional

router = APIRouter()

class YogaPlanRequest(BaseModel):
    session_type: str
    duration_minutes: int
    energy_trend: Optional[str] = "medium"
    stress_level: Optional[int] = 50

@router.post("/plan/{user_id}")
async def create_yoga_plan(user_id: int, request: YogaPlanRequest, db: Session = Depends(get_db)):
    """Create a yoga plan"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    yoga_agent = YogaAgent(db)
    plan = yoga_agent.generate_yoga_plan(
        user_id=user_id,
        session_type=request.session_type,
        duration_minutes=request.duration_minutes,
        energy_trend=request.energy_trend,
        stress_level=request.stress_level,
        yoga_experience=user.yoga_experience
    )
    
    return {
        "id": plan.id,
        "session_type": plan.session_type,
        "duration_minutes": plan.duration_minutes,
        "youtube_url": plan.youtube_url,
        "youtube_title": plan.youtube_title,
        "description": plan.description
    }

@router.post("/weekly/{user_id}")
async def create_weekly_plan(user_id: int, db: Session = Depends(get_db)):
    """Create weekly yoga plan"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    yoga_agent = YogaAgent(db)
    plans = yoga_agent.generate_weekly_plan(
        user_id=user_id,
        recommendations={"energy_trend": "medium", "stress_level": 50},
        yoga_experience=user.yoga_experience
    )
    
    return [{
        "id": p.id,
        "session_type": p.session_type,
        "duration_minutes": p.duration_minutes,
        "youtube_url": p.youtube_url,
        "youtube_title": p.youtube_title,
        "description": p.description
    } for p in plans]

@router.get("/plans/{user_id}")
async def get_yoga_plans(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Get user's yoga plans"""
    plans = db.query(YogaPlan).filter(
        YogaPlan.user_id == user_id
    ).order_by(YogaPlan.date.desc()).limit(limit).all()
    
    return plans

@router.get("/plans/{user_id}/today")
async def get_today_yoga_plan(user_id: int, db: Session = Depends(get_db)):
    """Get today's yoga plan"""
    from datetime import datetime, date
    today = date.today()
    
    plan = db.query(YogaPlan).filter(
        YogaPlan.user_id == user_id,
        YogaPlan.date >= datetime.combine(today, datetime.min.time())
    ).order_by(YogaPlan.date.desc()).first()
    
    if not plan:
        return {"message": "No yoga plan for today"}
    
    return {
        "id": plan.id,
        "session_type": plan.session_type,
        "duration_minutes": plan.duration_minutes,
        "youtube_url": plan.youtube_url,
        "youtube_title": plan.youtube_title,
        "youtube_video_id": plan.youtube_video_id,
        "description": plan.description
    }

