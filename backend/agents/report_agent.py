from typing import Dict, List
from sqlalchemy.orm import Session
from database import CheckIn, QuizResponse, NutritionPlan, YogaPlan, Progress
from datetime import datetime, timedelta
from sqlalchemy import func

class ReportAgent:
    """Generates weekly & monthly progress summaries with insights"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_weekly_report(self, user_id: int) -> Dict:
        """Generate weekly progress report"""
        today = datetime.utcnow().date()
        week_start = today - timedelta(days=7)
        
        # Collect data
        checkins = self.db.query(CheckIn).filter(
            CheckIn.user_id == user_id,
            CheckIn.date >= week_start
        ).all()
        
        quizzes = self.db.query(QuizResponse).filter(
            QuizResponse.user_id == user_id,
            QuizResponse.date >= week_start
        ).all()
        
        nutrition_plans = self.db.query(NutritionPlan).filter(
            NutritionPlan.user_id == user_id,
            NutritionPlan.date >= week_start
        ).all()
        
        yoga_plans = self.db.query(YogaPlan).filter(
            YogaPlan.user_id == user_id,
            YogaPlan.date >= week_start
        ).all()
        
        # Calculate metrics
        avg_adherence = sum(c.adherence for c in checkins) / len(checkins) if checkins else 0
        avg_stress = sum(q.stress_score for q in quizzes) / len(quizzes) if quizzes else 50
        avg_motivation = sum(q.motivation_score for q in quizzes) / len(quizzes) if quizzes else 50
        
        # Nutrition totals
        total_calories = sum(n.nutrients.get("calories", 0) for n in nutrition_plans if n.nutrients)
        total_protein = sum(n.nutrients.get("protein", 0) for n in nutrition_plans if n.nutrients)
        total_fiber = sum(n.nutrients.get("fiber", 0) for n in nutrition_plans if n.nutrients)
        
        # Yoga consistency
        yoga_days = len(yoga_plans)
        yoga_consistency = (yoga_days / 7) * 100
        
        # Insights
        insights = self._generate_insights(checkins, quizzes, nutrition_plans, yoga_plans)
        
        return {
            "period": "weekly",
            "start_date": week_start.isoformat(),
            "end_date": today.isoformat(),
            "metrics": {
                "adherence_avg": round(avg_adherence, 1),
                "stress_avg": round(avg_stress, 1),
                "motivation_avg": round(avg_motivation, 1),
                "yoga_consistency": round(yoga_consistency, 1),
                "nutrition": {
                    "total_calories": round(total_calories, 0),
                    "total_protein": round(total_protein, 1),
                    "total_fiber": round(total_fiber, 1),
                }
            },
            "insights": insights,
            "barriers_faced": self._identify_barriers(checkins, quizzes),
            "recommendations": self._generate_recommendations(avg_adherence, avg_stress, yoga_consistency)
        }
    
    def generate_monthly_report(self, user_id: int) -> Dict:
        """Generate monthly progress report"""
        today = datetime.utcnow().date()
        month_start = today - timedelta(days=30)
        
        # Similar to weekly but for 30 days
        checkins = self.db.query(CheckIn).filter(
            CheckIn.user_id == user_id,
            CheckIn.date >= month_start
        ).all()
        
        quizzes = self.db.query(QuizResponse).filter(
            QuizResponse.user_id == user_id,
            QuizResponse.date >= month_start
        ).all()
        
        nutrition_plans = self.db.query(NutritionPlan).filter(
            NutritionPlan.user_id == user_id,
            NutritionPlan.date >= month_start
        ).all()
        
        yoga_plans = self.db.query(YogaPlan).filter(
            YogaPlan.user_id == user_id,
            YogaPlan.date >= month_start
        ).all()
        
        # Trends
        stress_trend = self._calculate_trend([q.stress_score for q in quizzes])
        motivation_trend = self._calculate_trend([q.motivation_score for q in quizzes])
        adherence_trend = self._calculate_trend([c.adherence for c in checkins])
        
        return {
            "period": "monthly",
            "start_date": month_start.isoformat(),
            "end_date": today.isoformat(),
            "trends": {
                "stress": stress_trend,
                "motivation": motivation_trend,
                "adherence": adherence_trend,
            },
            "summary": {
                "total_checkins": len(checkins),
                "total_quizzes": len(quizzes),
                "total_meals": len(nutrition_plans),
                "total_yoga_sessions": len(yoga_plans),
            },
            "next_month_strategy": self._generate_next_month_strategy(
                stress_trend, motivation_trend, adherence_trend
            )
        }
    
    def _generate_insights(self, checkins, quizzes, nutrition_plans, yoga_plans) -> List[str]:
        """Generate insights from data"""
        insights = []
        
        if checkins:
            avg_sleep = sum(c.sleep_hours for c in checkins) / len(checkins)
            if avg_sleep < 6:
                insights.append("Sleep quality is below optimal. Consider earlier bedtime routines.")
            elif avg_sleep >= 8:
                insights.append("Great sleep consistency! This supports your wellness goals.")
        
        if quizzes:
            recent_stress = quizzes[-1].stress_score if quizzes else 50
            if recent_stress > 70:
                insights.append("Stress levels are elevated. Focus on gentle yoga and meditation.")
        
        if yoga_plans:
            if len(yoga_plans) >= 5:
                insights.append("Excellent yoga consistency! Keep up the momentum.")
            elif len(yoga_plans) < 3:
                insights.append("Consider increasing yoga frequency for better results.")
        
        return insights
    
    def _identify_barriers(self, checkins, quizzes) -> List[str]:
        """Identify barriers to adherence"""
        barriers = []
        
        if checkins:
            low_adherence_days = [c for c in checkins if c.adherence < 40]
            if len(low_adherence_days) > 2:
                barriers.append("Low adherence on multiple days - plans may be too complex")
        
        if quizzes:
            low_motivation = [q for q in quizzes if q.motivation_score < 40]
            if len(low_motivation) > 1:
                barriers.append("Motivation dips detected - consider reward-based planning")
        
        return barriers
    
    def _generate_recommendations(self, adherence: float, stress: float, yoga_consistency: float) -> List[str]:
        """Generate recommendations"""
        recommendations = []
        
        if adherence < 50:
            recommendations.append("Simplify meal plans to improve adherence")
        
        if stress > 70:
            recommendations.append("Increase stress-relief yoga sessions")
        
        if yoga_consistency < 50:
            recommendations.append("Try shorter yoga sessions (10-15 min) for better consistency")
        
        return recommendations
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend (improving, declining, stable)"""
        if len(values) < 2:
            return "insufficient_data"
        
        first_half = sum(values[:len(values)//2]) / (len(values)//2)
        second_half = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
        
        diff = second_half - first_half
        if diff > 5:
            return "improving"
        elif diff < -5:
            return "declining"
        else:
            return "stable"
    
    def _generate_next_month_strategy(self, stress_trend: str, motivation_trend: str, 
                                     adherence_trend: str) -> List[str]:
        """Generate strategy for next month"""
        strategy = []
        
        if stress_trend == "declining":
            strategy.append("Continue stress management focus - maintain meditation practices")
        elif stress_trend == "improving":
            strategy.append("Stress management is working - can gradually increase challenge")
        
        if adherence_trend == "declining":
            strategy.append("Simplify plans and focus on consistency over complexity")
        elif adherence_trend == "improving":
            strategy.append("Adherence improving - can introduce more variety")
        
        return strategy

