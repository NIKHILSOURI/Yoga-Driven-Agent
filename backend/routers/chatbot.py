import os
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, User
from typing import List, Optional
import openai
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    user_id: int

class ChatResponse(BaseModel):
    message: str
    role: str = "assistant"

@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        return {
            "message": "I'm a wellness coach focused on Sattvic nutrition and yoga. How can I help you today?",
            "role": "assistant"
        }
    
    try:
        client = openai.OpenAI(api_key=openai_api_key)
        
        system_prompt = f"""You are a Yoga-Driven Wellness & Nutrition Coach. You help users with:
- Sattvic nutrition (yoga-aligned, light, fresh, plant-based)
- Yoga practice recommendations
- Mental wellness support (non-clinical)
- Meal planning based on available ingredients
- Stress management through yoga and nutrition

User profile:
- Name: {user.name}
- Yoga experience: {user.yoga_experience}
- Dietary preferences: {user.dietary_preferences}
- Goals: {user.goals}

Remember:
- This is wellness advice, not medical advice
- Focus on Sattvic principles
- Be encouraging and supportive
- Suggest specific yoga practices when relevant
- Recommend nutrient-rich, plant-based meals
"""
        
        messages = [{"role": "system", "content": system_prompt}]
        for msg in request.messages:
            messages.append({"role": msg.role, "content": msg.content})
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
        except Exception as e:
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
            except Exception as e2:
                raise e2
        
        return {
            "message": response.choices[0].message.content,
            "role": "assistant"
        }
    except Exception as e:
        error_msg = str(e).lower()
        error_str = str(e)
        
        print(f"Chatbot error: {error_str}")
        
        if "quota" in error_msg or "429" in error_msg or "billing" in error_msg:
            user_query = request.messages[-1].content.lower() if request.messages else ""
            fallback_response = _get_fallback_response(user_query, user)
            return {
                "message": fallback_response,
                "role": "assistant"
            }
        
        if "model" in error_msg or "404" in error_msg or "not found" in error_msg:
            return {
                "message": "I'm here to help with your wellness journey! However, I'm experiencing some technical difficulties with the AI service. You can still use the other features like check-ins, nutrition planning, and yoga recommendations. Please try again later or contact support if the issue persists.",
                "role": "assistant"
            }
        
        user_query = request.messages[-1].content.lower() if request.messages else ""
        fallback_response = _get_fallback_response(user_query, user)
        return {
            "message": fallback_response,
            "role": "assistant"
        }

def _get_fallback_response(user_query: str, user) -> str:
    query_lower = user_query.lower()
    
    if any(word in query_lower for word in ["yoga", "pose", "practice", "stretch", "meditation"]):
        if "beginner" in query_lower or "start" in query_lower:
            return f"Great question! For beginners, I recommend starting with gentle yoga poses like Child's Pose (Balasana), Mountain Pose (Tadasana), and Cat-Cow stretches. Since you're at the {user.yoga_experience} level, you might enjoy a 15-20 minute morning routine focusing on flexibility and breathing. Would you like me to suggest a specific yoga plan for today?"
        elif "stress" in query_lower or "relax" in query_lower:
            return "For stress relief, I recommend restorative yoga poses like Legs Up the Wall, Child's Pose, and Corpse Pose (Savasana). Combine this with deep breathing exercises - try alternate nostril breathing (Nadi Shodhana) for 5 minutes. A gentle 20-30 minute evening practice can work wonders for relaxation."
        else:
            return f"Yoga is wonderful for overall wellness! Based on your {user.yoga_experience} experience level, I'd suggest focusing on poses that align with your goals. For flexibility, try forward folds and twists. For strength, incorporate Warrior poses and Plank. Would you like specific recommendations?"
    
    if any(word in query_lower for word in ["food", "meal", "nutrition", "eat", "diet", "recipe", "ingredient"]):
        if "sattvic" in query_lower or "yoga" in query_lower:
            return "Sattvic nutrition focuses on fresh, light, plant-based foods that promote clarity and energy. Great options include: fresh fruits, vegetables, whole grains (brown rice, oats), legumes (lentils, mung beans), nuts, seeds, and dairy products like ghee and fresh milk. Avoid processed foods, onions, garlic, and overly spicy foods. Would you like a specific meal plan?"
        elif "breakfast" in query_lower:
            return "A Sattvic breakfast could include: oatmeal with fresh fruits and honey, fresh fruit salad, or a smoothie with banana, dates, and nuts. These provide sustained energy without heaviness."
        elif "lunch" in query_lower:
            return "For lunch, consider: brown rice with dal (lentils), steamed vegetables, fresh salad, and roti (whole wheat flatbread). This combination provides protein, fiber, and essential nutrients."
        elif "dinner" in query_lower:
            return "A light Sattvic dinner might include: vegetable soup, steamed vegetables, or a simple khichdi (rice and lentils). Keep dinner light and early (ideally 2-3 hours before sleep) for better digestion."
        else:
            return f"Based on your dietary preferences ({user.dietary_preferences}), I can help you plan nutritious, Sattvic meals. Focus on fresh, whole foods that align with your goals: {user.goals}. Would you like specific recipe suggestions?"
    
    if any(word in query_lower for word in ["wellness", "health", "feel", "energy", "tired", "sleep"]):
        return "Wellness is a holistic journey! Combine daily yoga practice (even 15-20 minutes), Sattvic nutrition, adequate sleep (7-8 hours), and mindfulness. Start with small, consistent habits - perhaps a morning yoga routine and mindful eating. How can I help you create a personalized wellness plan?"
    
    return f"Namaste {user.name}! I'm here to help with your wellness journey. I can assist with:\n\n• Yoga practice recommendations based on your {user.yoga_experience} level\n• Sattvic nutrition and meal planning\n• Wellness tips and guidance\n• Stress management through yoga and nutrition\n\nWhat would you like to explore today? Feel free to ask about specific yoga poses, meal ideas, or wellness practices!"

