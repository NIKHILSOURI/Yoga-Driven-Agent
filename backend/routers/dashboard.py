from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, CheckIn, QuizResponse, NutritionPlan, YogaPlan, Progress
from datetime import datetime, timedelta
from sqlalchemy import func

router = APIRouter()

@router.get("/{user_id}/overview")
async def get_dashboard_overview(user_id: int, db: Session = Depends(get_db)):
    """Get dashboard overview data"""
    today = datetime.utcnow().date()
    week_start = today - timedelta(days=7)
    
    # Yoga streak
    recent_yoga = db.query(YogaPlan).filter(
        YogaPlan.user_id == user_id,
        YogaPlan.date >= week_start
    ).all()
    
    yoga_streak = len(recent_yoga)
    yoga_consistency = (yoga_streak / 7) * 100
    
    # Recent check-ins
    recent_checkins = db.query(CheckIn).filter(
        CheckIn.user_id == user_id,
        CheckIn.date >= week_start
    ).all()
    
    avg_adherence = sum(c.adherence for c in recent_checkins) / len(recent_checkins) if recent_checkins else 0
    
    # Nutrition totals
    recent_nutrition = db.query(NutritionPlan).filter(
        NutritionPlan.user_id == user_id,
        NutritionPlan.date >= week_start
    ).all()
    
    total_protein = sum(n.nutrients.get("protein", 0) for n in recent_nutrition if n.nutrients)
    total_fiber = sum(n.nutrients.get("fiber", 0) for n in recent_nutrition if n.nutrients)
    total_calcium = sum(n.nutrients.get("calcium", 0) for n in recent_nutrition if n.nutrients)
    
    # Stress trend
    recent_quizzes = db.query(QuizResponse).filter(
        QuizResponse.user_id == user_id,
        QuizResponse.date >= week_start
    ).all()
    
    avg_stress = sum(q.stress_score for q in recent_quizzes) / len(recent_quizzes) if recent_quizzes else 50
    stress_reduction = 100 - avg_stress if avg_stress else 0
    
    # Adherence improvement
    if len(recent_checkins) >= 2:
        first_half = sum(c.adherence for c in recent_checkins[:len(recent_checkins)//2]) / (len(recent_checkins)//2)
        second_half = sum(c.adherence for c in recent_checkins[len(recent_checkins)//2:]) / (len(recent_checkins) - len(recent_checkins)//2)
        adherence_improvement = second_half - first_half
    else:
        adherence_improvement = 0
    
    return {
        "yoga": {
            "streak": yoga_streak,
            "consistency_percentage": round(yoga_consistency, 1)
        },
        "nutrition": {
            "protein_total": round(total_protein, 1),
            "fiber_total": round(total_fiber, 1),
            "calcium_total": round(total_calcium, 1)
        },
        "wellness": {
            "stress_reduction": round(stress_reduction, 1),
            "adherence_avg": round(avg_adherence, 1),
            "adherence_improvement": round(adherence_improvement, 1)
        },
        "period": {
            "start": week_start.isoformat(),
            "end": today.isoformat()
        }
    }

@router.get("/{user_id}/trends")
async def get_trends(user_id: int, days: int = 30, db: Session = Depends(get_db)):
    """Get trend data for charts"""
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=days)
    
    # Daily data points
    checkins = db.query(CheckIn).filter(
        CheckIn.user_id == user_id,
        CheckIn.date >= start_date
    ).order_by(CheckIn.date).all()
    
    quizzes = db.query(QuizResponse).filter(
        QuizResponse.user_id == user_id,
        QuizResponse.date >= start_date
    ).order_by(QuizResponse.date).all()
    
    nutrition = db.query(NutritionPlan).filter(
        NutritionPlan.user_id == user_id,
        NutritionPlan.date >= start_date
    ).order_by(NutritionPlan.date).all()
    
    # Format dates properly and ensure data exists
    adherence_data = [{"date": c.date.isoformat(), "value": float(c.adherence)} for c in checkins] if checkins else []
    stress_data = [{"date": q.date.isoformat(), "value": int(q.stress_score)} for q in quizzes] if quizzes else []
    motivation_data = [{"date": q.date.isoformat(), "value": int(q.motivation_score)} for q in quizzes] if quizzes else []
    protein_data = [{"date": n.date.isoformat(), "value": float(n.nutrients.get("protein", 0))} for n in nutrition if n.nutrients] if nutrition else []
    fiber_data = [{"date": n.date.isoformat(), "value": float(n.nutrients.get("fiber", 0))} for n in nutrition if n.nutrients] if nutrition else []
    
    return {
        "adherence": adherence_data,
        "stress": stress_data,
        "motivation": motivation_data,
        "protein": protein_data,
        "fiber": fiber_data,
    }

@router.get("/{user_id}/top-items")
async def get_top_items(user_id: int, db: Session = Depends(get_db)):
    """Get top liked meals and videos"""
    # This would typically come from user feedback/memory
    # For now, return most frequent items
    recent_nutrition = db.query(NutritionPlan).filter(
        NutritionPlan.user_id == user_id
    ).order_by(NutritionPlan.date.desc()).limit(20).all()
    
    recent_yoga = db.query(YogaPlan).filter(
        YogaPlan.user_id == user_id
    ).order_by(YogaPlan.date.desc()).limit(10).all()
    
    # Count recipe frequency
    recipe_counts = {}
    for plan in recent_nutrition:
        name = plan.recipe_name
        recipe_counts[name] = recipe_counts.get(name, 0) + 1
    
    top_meals = sorted(recipe_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "top_meals": [{"name": name, "count": count} for name, count in top_meals],
        "recent_videos": [{
            "title": p.youtube_title,
            "url": p.youtube_url,
            "session_type": p.session_type
        } for p in recent_yoga[:5]]
    }

