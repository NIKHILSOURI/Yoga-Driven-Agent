from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, CheckIn, User
from datetime import datetime
from typing import Optional
from agents.observe_agent import ObserveAgent
from agents.reasoner_agent import ReasonerAgent
from agents.nutrition_agent import NutritionAgent
from agents.yoga_agent import YogaAgent
from agents.fairness_agent import FairnessAgent

router = APIRouter()

class CheckInData(BaseModel):
    mood: str
    mood_score: int
    appetite: float
    energy: float
    sleep_hours: float
    adherence: float
    ingredients: Optional[str] = ""
    notes: Optional[str] = ""

@router.post("/{user_id}")
async def submit_checkin(user_id: int, checkin_data: CheckInData, db: Session = Depends(get_db)):
    """Submit daily check-in and trigger agentic planning"""
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Save check-in
    checkin = CheckIn(
        user_id=user_id,
        date=datetime.utcnow(),
        **checkin_data.dict()
    )
    db.add(checkin)
    db.commit()
    
    # Trigger agentic system
    reasoner = ReasonerAgent(db)
    reasoning_result = reasoner.reason(user_id)
    
    # Generate plans based on reasoning
    nutrition_agent = NutritionAgent(db)
    yoga_agent = YogaAgent(db)
    fairness_agent = FairnessAgent(db)
    
    plans = {
        "nutrition": [],
        "yoga": None
    }
    
    # Generate nutrition plans if ingredients provided
    if checkin_data.ingredients:
        ingredients_list = [ing.strip() for ing in checkin_data.ingredients.split(",") if ing.strip()]
        if ingredients_list:
            # Check API quota
            quota_check = fairness_agent.check_api_quota("usda", user_id)
            if quota_check["allowed"]:
                # Generate complete daily meal plan: breakfast, lunch, dinner, and snacks
                meal_types = ["breakfast", "lunch", "dinner", "snack"]
                
                # Distribute ingredients intelligently across meals
                total_ingredients = len(ingredients_list)
                ingredients_per_meal = max(3, total_ingredients // len(meal_types))
                
                for idx, meal_type in enumerate(meal_types):
                    try:
                        # Distribute ingredients across meals
                        start_idx = idx * ingredients_per_meal
                        end_idx = start_idx + ingredients_per_meal if idx < len(meal_types) - 1 else total_ingredients
                        meal_ingredients = ingredients_list[start_idx:end_idx]
                        
                        # Ensure each meal has at least some ingredients
                        if not meal_ingredients and ingredients_list:
                            # For snacks, use remaining ingredients or a subset
                            if meal_type == "snack":
                                meal_ingredients = ingredients_list[-3:] if len(ingredients_list) >= 3 else ingredients_list
                            else:
                                meal_ingredients = ingredients_list[:3] if len(ingredients_list) >= 3 else ingredients_list
                        
                        if meal_ingredients:
                            plan = nutrition_agent.create_nutrition_plan(
                                user_id=user_id,
                                meal_type=meal_type,
                                ingredients=meal_ingredients,
                                recommendations=reasoning_result["recommendations"]
                            )
                            plans["nutrition"].append({
                                "id": plan.id,
                                "meal_type": plan.meal_type,
                                "recipe_name": plan.recipe_name,
                                "nutrients": plan.nutrients,
                                "instructions": plan.recipe_instructions,
                                "ingredients": plan.ingredients,
                                "sattvic_score": plan.sattvic_score,
                                "simplicity_index": plan.meal_simplicity_index
                            })
                            fairness_agent.record_api_call("usda", user_id)
                    except Exception as e:
                        print(f"Error creating {meal_type} plan: {str(e)}")
                        continue
    
    # Generate yoga plan
    quota_check = fairness_agent.check_api_quota("youtube", user_id)
    if quota_check["allowed"]:
        try:
            yoga_plan = yoga_agent.generate_yoga_plan(
                user_id=user_id,
                session_type=reasoning_result["recommendations"]["yoga"]["session_type"],
                duration_minutes=reasoning_result["recommendations"]["yoga"]["duration_minutes"],
                energy_trend=reasoning_result["energy_trend"],
                stress_level=reasoning_result.get("rules_triggered", [{}])[0].get("condition", "50") if reasoning_result.get("rules_triggered") else 50,
                yoga_experience=user.yoga_experience
            )
            plans["yoga"] = {
                "id": yoga_plan.id,
                "session_type": yoga_plan.session_type,
                "duration_minutes": yoga_plan.duration_minutes,
                "youtube_url": yoga_plan.youtube_url,
                "youtube_title": yoga_plan.youtube_title,
                "description": yoga_plan.description
            }
            fairness_agent.record_api_call("youtube", user_id)
        except Exception as e:
            pass
    
    return {
        "checkin_id": checkin.id,
        "reasoning": reasoning_result,
        "plans": plans
    }

@router.get("/{user_id}/recent")
async def get_recent_checkins(user_id: int, limit: int = 7, db: Session = Depends(get_db)):
    """Get recent check-ins"""
    checkins = db.query(CheckIn).filter(
        CheckIn.user_id == user_id
    ).order_by(CheckIn.date.desc()).limit(limit).all()
    
    return checkins

