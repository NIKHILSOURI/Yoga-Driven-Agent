from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, DecisionTrace, User
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/{user_id}/recent")
async def get_recent_traces(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Get recent decision traces"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    traces = db.query(DecisionTrace).filter(
        DecisionTrace.user_id == user_id
    ).order_by(DecisionTrace.date.desc()).limit(limit).all()
    
    return [{
        "id": t.id,
        "date": t.date.isoformat(),
        "agent_name": t.agent_name,
        "triggered_rules": t.triggered_rules,
        "memory_retrieved": t.memory_retrieved,
        "plan_chosen": t.plan_chosen,
        "tools_called": t.tools_called,
        "explanation": t.explanation
    } for t in traces]

@router.get("/{user_id}/today")
async def get_today_traces(user_id: int, db: Session = Depends(get_db)):
    """Get today's decision traces"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    today = datetime.utcnow().date()
    
    traces = db.query(DecisionTrace).filter(
        DecisionTrace.user_id == user_id,
        DecisionTrace.date >= datetime.combine(today, datetime.min.time())
    ).order_by(DecisionTrace.date.desc()).all()
    
    return [{
        "id": t.id,
        "date": t.date.isoformat(),
        "agent_name": t.agent_name,
        "triggered_rules": t.triggered_rules,
        "memory_retrieved": t.memory_retrieved,
        "plan_chosen": t.plan_chosen,
        "tools_called": t.tools_called,
        "explanation": t.explanation
    } for t in traces]

