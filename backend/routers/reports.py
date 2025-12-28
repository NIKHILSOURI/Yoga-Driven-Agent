from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, User
from agents.report_agent import ReportAgent

router = APIRouter()

@router.get("/weekly/{user_id}")
async def get_weekly_report(user_id: int, db: Session = Depends(get_db)):
    """Generate weekly report"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    report_agent = ReportAgent(db)
    report = report_agent.generate_weekly_report(user_id)
    
    return report

@router.get("/monthly/{user_id}")
async def get_monthly_report(user_id: int, db: Session = Depends(get_db)):
    """Generate monthly report"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    report_agent = ReportAgent(db)
    report = report_agent.generate_monthly_report(user_id)
    
    return report

