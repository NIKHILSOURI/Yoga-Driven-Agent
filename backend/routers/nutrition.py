from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, NutritionPlan, User
from agents.nutrition_agent import NutritionAgent
from typing import List, Optional

router = APIRouter()

class IngredientLookup(BaseModel):
    ingredient: str

class RecipeRequest(BaseModel):
    ingredients: List[str]
    meal_type: str
    focus: Optional[str] = "balanced_sattvic"

@router.get("/lookup/{ingredient}")
async def lookup_nutrient(ingredient: str, db: Session = Depends(get_db)):
    """Lookup nutrients for an ingredient"""
    nutrition_agent = NutritionAgent(db)
    result = nutrition_agent.lookup_nutrients(ingredient)
    return result

@router.post("/recipe/generate")
async def generate_recipe(request: RecipeRequest, db: Session = Depends(get_db)):
    """Generate a recipe"""
    nutrition_agent = NutritionAgent(db)
    result = nutrition_agent.generate_recipe(
        ingredients=request.ingredients,
        meal_type=request.meal_type,
        focus=request.focus
    )
    return result

@router.get("/plans/{user_id}")
async def get_nutrition_plans(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Get user's nutrition plans"""
    plans = db.query(NutritionPlan).filter(
        NutritionPlan.user_id == user_id
    ).order_by(NutritionPlan.date.desc()).limit(limit).all()
    
    return plans

@router.get("/plans/{user_id}/today")
async def get_today_plans(user_id: int, db: Session = Depends(get_db)):
    """Get today's nutrition plans"""
    from datetime import datetime, date
    today = date.today()
    
    plans = db.query(NutritionPlan).filter(
        NutritionPlan.user_id == user_id,
        NutritionPlan.date >= datetime.combine(today, datetime.min.time())
    ).order_by(NutritionPlan.date.desc()).all()
    
    return [{
        "id": p.id,
        "meal_type": p.meal_type,
        "recipe_name": p.recipe_name,
        "ingredients": p.ingredients if p.ingredients else [],
        "nutrients": p.nutrients if p.nutrients else {},
        "recipe_instructions": p.recipe_instructions,
        "sattvic_score": p.sattvic_score,
        "meal_simplicity_index": p.meal_simplicity_index,
        "date": p.date.isoformat() if p.date else None
    } for p in plans]

