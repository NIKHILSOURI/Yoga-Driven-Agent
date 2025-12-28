"""
Database utility functions for querying and managing data.
"""
from sqlalchemy.orm import Session
from database import get_db, User, CheckIn, QuizResponse, NutritionPlan, YogaPlan, Progress, Memory
from datetime import datetime, timedelta
from typing import Optional, List, Dict

def get_user_stats(db: Session, user_id: int) -> Dict:
    """Get comprehensive user statistics"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    
    # Count records
    checkin_count = db.query(CheckIn).filter(CheckIn.user_id == user_id).count()
    quiz_count = db.query(QuizResponse).filter(QuizResponse.user_id == user_id).count()
    nutrition_count = db.query(NutritionPlan).filter(NutritionPlan.user_id == user_id).count()
    yoga_count = db.query(YogaPlan).filter(YogaPlan.user_id == user_id).count()
    
    # Recent activity
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_checkins = db.query(CheckIn).filter(
        CheckIn.user_id == user_id,
        CheckIn.date >= week_ago
    ).count()
    
    return {
        "user_id": user_id,
        "name": user.name,
        "email": user.email,
        "stats": {
            "total_checkins": checkin_count,
            "total_quizzes": quiz_count,
            "total_meals": nutrition_count,
            "total_yoga_sessions": yoga_count,
            "recent_checkins_7d": recent_checkins,
        },
        "profile": {
            "yoga_experience": user.yoga_experience,
            "goals": user.goals,
            "dietary_preferences": user.dietary_preferences,
        }
    }

def get_recent_activity(db: Session, user_id: int, days: int = 7) -> Dict:
    """Get recent user activity"""
    since = datetime.utcnow() - timedelta(days=days)
    
    checkins = db.query(CheckIn).filter(
        CheckIn.user_id == user_id,
        CheckIn.date >= since
    ).order_by(CheckIn.date.desc()).all()
    
    quizzes = db.query(QuizResponse).filter(
        QuizResponse.user_id == user_id,
        QuizResponse.date >= since
    ).order_by(QuizResponse.date.desc()).all()
    
    nutrition = db.query(NutritionPlan).filter(
        NutritionPlan.user_id == user_id,
        NutritionPlan.date >= since
    ).order_by(NutritionPlan.date.desc()).all()
    
    yoga = db.query(YogaPlan).filter(
        YogaPlan.user_id == user_id,
        YogaPlan.date >= since
    ).order_by(YogaPlan.date.desc()).all()
    
    return {
        "checkins": [{
            "date": c.date.isoformat(),
            "mood": c.mood,
            "energy": c.energy,
            "adherence": c.adherence
        } for c in checkins],
        "quizzes": [{
            "date": q.date.isoformat(),
            "stress": q.stress_score,
            "motivation": q.motivation_score
        } for q in quizzes],
        "nutrition_plans": len(nutrition),
        "yoga_plans": len(yoga)
    }

def cleanup_old_data(db: Session, days: int = 90):
    """Clean up data older than specified days (for maintenance)"""
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    # This is a utility function - be careful with deletions!
    # Uncomment to use:
    # deleted_checkins = db.query(CheckIn).filter(CheckIn.date < cutoff).delete()
    # db.commit()
    # return {"deleted_checkins": deleted_checkins}
    pass

if __name__ == "__main__":
    # Example usage
    from database import SessionLocal
    
    db = SessionLocal()
    try:
        # Get all users
        users = db.query(User).all()
        print(f"Total users: {len(users)}")
        
        for user in users:
            stats = get_user_stats(db, user.id)
            if stats:
                print(f"\n{stats['name']} ({stats['email']}):")
                print(f"  Check-ins: {stats['stats']['total_checkins']}")
                print(f"  Quizzes: {stats['stats']['total_quizzes']}")
                print(f"  Meals: {stats['stats']['total_meals']}")
                print(f"  Yoga sessions: {stats['stats']['total_yoga_sessions']}")
    finally:
        db.close()

