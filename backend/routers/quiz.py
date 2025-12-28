from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, QuizResponse, User
from datetime import datetime
from typing import Dict, List

router = APIRouter()

class QuizSubmission(BaseModel):
    responses: Dict[str, int]  # question_id: answer_score

@router.post("/{user_id}")
async def submit_quiz(user_id: int, quiz_data: QuizSubmission, db: Session = Depends(get_db)):
    """Submit mental health quiz"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate scores (simplified - in production would have proper question mapping)
    responses = quiz_data.responses
    
    stress_score = responses.get("stress", 50)
    anxiety_score = responses.get("anxiety", 50)
    motivation_score = responses.get("motivation", 50)
    mindfulness_score = responses.get("mindfulness", 50)
    appetite_indicator = responses.get("appetite", 50)
    sleep_quality = responses.get("sleep", 50)
    
    total_score = (stress_score + anxiety_score + motivation_score + 
                  mindfulness_score + appetite_indicator + sleep_quality) // 6
    
    quiz_response = QuizResponse(
        user_id=user_id,
        date=datetime.utcnow(),
        stress_score=stress_score,
        anxiety_score=anxiety_score,
        motivation_score=motivation_score,
        mindfulness_score=mindfulness_score,
        appetite_indicator=appetite_indicator,
        sleep_quality=sleep_quality,
        total_score=total_score,
        responses=responses
    )
    
    db.add(quiz_response)
    db.commit()
    db.refresh(quiz_response)
    
    return {
        "id": quiz_response.id,
        "scores": {
            "stress": stress_score,
            "anxiety": anxiety_score,
            "motivation": motivation_score,
            "mindfulness": mindfulness_score,
            "appetite": appetite_indicator,
            "sleep": sleep_quality,
            "total": total_score
        },
        "date": quiz_response.date.isoformat()
    }

@router.get("/{user_id}/recent")
async def get_recent_quizzes(user_id: int, limit: int = 5, db: Session = Depends(get_db)):
    """Get recent quiz responses"""
    quizzes = db.query(QuizResponse).filter(
        QuizResponse.user_id == user_id
    ).order_by(QuizResponse.date.desc()).limit(limit).all()
    
    return [{
        "id": q.id,
        "date": q.date.isoformat(),
        "scores": {
            "stress": q.stress_score,
            "anxiety": q.anxiety_score,
            "motivation": q.motivation_score,
            "mindfulness": q.mindfulness_score,
            "appetite": q.appetite_indicator,
            "sleep": q.sleep_quality,
            "total": q.total_score
        }
    } for q in quizzes]

@router.get("/questions")
async def get_quiz_questions():
    """Get quiz questions"""
    return {
        "questions": [
            {
                "id": "stress",
                "question": "How stressed do you feel today?",
                "scale": "1-10",
                "category": "stress"
            },
            {
                "id": "anxiety",
                "question": "Rate your anxiety level",
                "scale": "1-10",
                "category": "anxiety"
            },
            {
                "id": "motivation",
                "question": "How motivated are you today?",
                "scale": "1-10",
                "category": "motivation"
            },
            {
                "id": "mindfulness",
                "question": "How mindful/present do you feel?",
                "scale": "1-10",
                "category": "mindfulness"
            },
            {
                "id": "appetite",
                "question": "How is your appetite?",
                "scale": "1-10",
                "category": "appetite"
            },
            {
                "id": "sleep",
                "question": "How was your sleep quality last night?",
                "scale": "1-10",
                "category": "sleep"
            }
        ]
    }

