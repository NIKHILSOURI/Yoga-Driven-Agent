from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import CheckIn, QuizResponse, NutritionPlan, YogaPlan, Memory, MLPrediction

class ObserveAgent:
    """Collects user data: sleep, mood, ingredients, adherence, quiz scores"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def collect_daily_data(self, user_id: int) -> Dict:
        """Collects all relevant data for the day"""
        today = datetime.utcnow().date()
        
        # Get latest check-in
        checkin = self.db.query(CheckIn).filter(
            CheckIn.user_id == user_id
        ).order_by(CheckIn.date.desc()).first()
        
        # Get latest quiz
        quiz = self.db.query(QuizResponse).filter(
            QuizResponse.user_id == user_id
        ).order_by(QuizResponse.date.desc()).first()
        
        # Get last 3 days adherence
        three_days_ago = today - timedelta(days=3)
        recent_checkins = self.db.query(CheckIn).filter(
            CheckIn.user_id == user_id,
            CheckIn.date >= three_days_ago
        ).all()
        
        adherence_avg = sum(c.adherence for c in recent_checkins) / len(recent_checkins) if recent_checkins else 0
        
        # Get recent plans
        recent_nutrition = self.db.query(NutritionPlan).filter(
            NutritionPlan.user_id == user_id,
            NutritionPlan.date >= three_days_ago
        ).all()
        
        recent_yoga = self.db.query(YogaPlan).filter(
            YogaPlan.user_id == user_id,
            YogaPlan.date >= three_days_ago
        ).all()
        
        # Get preferences from memory
        preferences = self.db.query(Memory).filter(
            Memory.user_id == user_id,
            Memory.memory_type.in_(["preference", "liked_meal", "disliked_meal"])
        ).all()
        
        return {
            "checkin": {
                "sleep_hours": checkin.sleep_hours if checkin else 7.0,
                "mood_score": checkin.mood_score if checkin else 5,
                "appetite": checkin.appetite if checkin else 5.0,
                "energy": checkin.energy if checkin else 5.0,
                "ingredients": checkin.ingredients if checkin else "",
            } if checkin else {
                "sleep_hours": 7.0,
                "mood_score": 5,
                "appetite": 5.0,
                "energy": 5.0,
                "ingredients": "",
            },
            "quiz": {
                "stress_score": quiz.stress_score if quiz else 50,
                "motivation_score": quiz.motivation_score if quiz else 50,
                "anxiety_score": quiz.anxiety_score if quiz else 50,
                "mindfulness_score": quiz.mindfulness_score if quiz else 50,
            } if quiz else {
                "stress_score": 50,
                "motivation_score": 50,
                "anxiety_score": 50,
                "mindfulness_score": 50,
            },
            "adherence": {
                "last_3_days_avg": adherence_avg,
                "recent_checkins_count": len(recent_checkins),
            },
            "recent_plans": {
                "nutrition_count": len(recent_nutrition),
                "yoga_count": len(recent_yoga),
            },
            "preferences": [p.content for p in preferences],
            "day_type": self._determine_day_type(),
        }
    
    def _determine_day_type(self) -> str:
        """Determines if it's weekday, weekend, etc."""
        today = datetime.utcnow()
        weekday = today.weekday()
        if weekday < 5:
            return "weekday"
        else:
            return "weekend"

