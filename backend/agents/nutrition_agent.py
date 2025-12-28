import os
import requests
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from database import NutritionPlan, Memory
from datetime import datetime
from dotenv import load_dotenv
import openai

load_dotenv()

class NutritionAgent:
    """Nutrient lookup, recipe generation, substitutions, macro aggregation"""
    
    def __init__(self, db: Session):
        self.db = db
        self.usda_api_key = os.getenv("USDA_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = openai.OpenAI(api_key=self.openai_api_key) if self.openai_api_key else None
    
    def lookup_nutrients(self, ingredient: str) -> Dict:
        """Lookup nutrients for an ingredient using USDA API"""
        try:
            # USDA FoodData Central API
            url = "https://api.nal.usda.gov/fdc/v1/foods/search"
            params = {
                "api_key": self.usda_api_key,
                "query": ingredient,
                "pageSize": 1
            }
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("foods") and len(data["foods"]) > 0:
                    food = data["foods"][0]
                    nutrients = {}
                    
                    # Extract key nutrients
                    for nutrient in food.get("foodNutrients", []):
                        nutrient_name = nutrient.get("nutrientName", "").lower()
                        value = nutrient.get("value", 0)
                        
                        if "energy" in nutrient_name or "calories" in nutrient_name:
                            nutrients["calories"] = value
                        elif "protein" in nutrient_name:
                            nutrients["protein"] = value
                        elif "fiber" in nutrient_name:
                            nutrients["fiber"] = value
                        elif "calcium" in nutrient_name:
                            nutrients["calcium"] = value
                        elif "iron" in nutrient_name:
                            nutrients["iron"] = value
                        elif "magnesium" in nutrient_name:
                            nutrients["magnesium"] = value
                    
                    return {
                        "success": True,
                        "ingredient": ingredient,
                        "nutrients": nutrients,
                        "food_name": food.get("description", ingredient)
                    }
            
            return {"success": False, "error": "No data found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_recipe(self, ingredients: List[str], meal_type: str, 
                       focus: str = "balanced_sattvic", user_preferences: Optional[Dict] = None) -> Dict:
        """Generate a Sattvic recipe using OpenAI"""
        if not self.openai_client:
            return self._generate_fallback_recipe(ingredients, meal_type, focus)
        
        try:
            # Meal-specific guidance
            meal_guidance = {
                "breakfast": "Light, energizing, easy to digest. Include whole grains, fruits, or light proteins. Good for starting the day.",
                "lunch": "Balanced, substantial but not heavy. Include vegetables, grains, legumes, or light proteins. Main meal of the day.",
                "dinner": "Light, easy to digest, should not be too heavy before sleep. Include vegetables, soups, or light grains. Keep it simple.",
                "snack": "Small, nutrient-dense, satisfying. Include fruits, nuts, seeds, or light options. Perfect for between meals."
            }
            
            prompt = f"""Generate a {meal_type} recipe that is Sattvic (yoga-aligned, light, fresh, plant-based, gut-friendly).

Ingredients available: {', '.join(ingredients)}
Focus: {focus}
Meal type: {meal_type}
Meal guidance: {meal_guidance.get(meal_type, 'Balanced and nutritious')}

Requirements:
- Sattvic principles: fresh, natural, minimally processed
- High fiber, moderate protein
- Include magnesium-rich foods if possible
- Easy to prepare
- Mindful eating friendly
- Use the provided ingredients creatively
- Appropriate portion size for {meal_type}

Provide:
1. Recipe name (creative and descriptive)
2. List of ingredients with quantities (use the provided ingredients)
3. Step-by-step instructions (clear and simple)
4. Estimated preparation time in minutes
5. Sattvic score (1-10, where 10 is most Sattvic)
6. Meal simplicity index (1-10, where 10 is easiest to prepare)

Format as JSON with keys: name, ingredients, instructions, prep_time_minutes, sattvic_score, simplicity_index"""
            
            # Try gpt-4o-mini first, fallback to gpt-3.5-turbo
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a Sattvic nutrition expert. Generate healthy, yoga-aligned recipes."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
            except Exception as e:
                # Fallback to gpt-3.5-turbo
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a Sattvic nutrition expert. Generate healthy, yoga-aligned recipes."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
            
            import json
            recipe_text = response.choices[0].message.content
            
            # Try to parse JSON from response
            try:
                recipe = json.loads(recipe_text)
            except:
                # Fallback if not pure JSON
                recipe = self._parse_recipe_text(recipe_text, ingredients, meal_type)
            
            # Calculate nutrients
            nutrients = self._calculate_recipe_nutrients(recipe.get("ingredients", []))
            
            return {
                "success": True,
                "recipe": recipe,
                "nutrients": nutrients,
                "meal_type": meal_type,
                "focus": focus
            }
        except Exception as e:
            return self._generate_fallback_recipe(ingredients, meal_type, focus)
    
    def _generate_fallback_recipe(self, ingredients: List[str], meal_type: str, focus: str) -> Dict:
        """Fallback recipe generator without OpenAI"""
        recipe_name = f"Sattvic {meal_type.title()} with {', '.join(ingredients[:3])}"
        
        instructions = f"""
1. Wash and prepare all ingredients
2. Heat a pan with minimal oil
3. Add ingredients in order of cooking time
4. Cook until tender and aromatic
5. Season with natural spices (turmeric, cumin, coriander)
6. Serve warm and mindfully
"""
        
        return {
            "success": True,
            "recipe": {
                "name": recipe_name,
                "ingredients": [{"name": ing, "quantity": "as needed"} for ing in ingredients],
                "instructions": instructions.strip(),
                "prep_time_minutes": 20,
                "sattvic_score": 7.5,
                "simplicity_index": 8.0
            },
            "nutrients": {
                "calories": 300,
                "protein": 15,
                "fiber": 8,
                "calcium": 100,
                "iron": 3,
                "magnesium": 50
            },
            "meal_type": meal_type,
            "focus": focus
        }
    
    def _parse_recipe_text(self, text: str, ingredients: List[str], meal_type: str) -> Dict:
        """Parse recipe from text response"""
        return {
            "name": f"Sattvic {meal_type}",
            "ingredients": [{"name": ing, "quantity": "as needed"} for ing in ingredients],
            "instructions": text[:500],
            "prep_time_minutes": 20,
            "sattvic_score": 7.5,
            "simplicity_index": 8.0
        }
    
    def _calculate_recipe_nutrients(self, ingredients: List[Dict]) -> Dict:
        """Calculate total nutrients for recipe"""
        total = {
            "calories": 0,
            "protein": 0,
            "fiber": 0,
            "calcium": 0,
            "iron": 0,
            "magnesium": 0
        }
        
        for ing in ingredients[:5]:  # Limit to avoid too many API calls
            ing_name = ing.get("name", "")
            result = self.lookup_nutrients(ing_name)
            if result.get("success"):
                nutrients = result.get("nutrients", {})
                for key in total:
                    total[key] += nutrients.get(key, 0)
        
        return total
    
    def create_nutrition_plan(self, user_id: int, meal_type: str, ingredients: List[str],
                             recommendations: Dict) -> NutritionPlan:
        """Create and save a nutrition plan"""
        focus = recommendations.get("nutrition", {}).get("focus", "balanced_sattvic")
        
        # Get user preferences
        user_prefs = self.db.query(Memory).filter(
            Memory.user_id == user_id,
            Memory.memory_type == "preference"
        ).first()
        
        recipe_data = self.generate_recipe(ingredients, meal_type, focus, 
                                         user_prefs.content if user_prefs else None)
        
        plan = NutritionPlan(
            user_id=user_id,
            date=datetime.utcnow(),
            meal_type=meal_type,
            recipe_name=recipe_data["recipe"]["name"],
            ingredients=[ing.get("name", "") for ing in recipe_data["recipe"]["ingredients"]],
            nutrients=recipe_data["nutrients"],
            recipe_instructions=recipe_data["recipe"]["instructions"],
            meal_simplicity_index=recipe_data["recipe"].get("simplicity_index", 7.0),
            sattvic_score=recipe_data["recipe"].get("sattvic_score", 7.0),
            created_by_agent="NutritionAgent"
        )
        
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        
        return plan

