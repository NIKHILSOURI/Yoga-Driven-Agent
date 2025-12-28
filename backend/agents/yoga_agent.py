import os
import requests
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from database import YogaPlan
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class YogaAgent:
    """Daily/weekly yoga plan + YouTube video recommendations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    
    def search_youtube_video(self, query: str, duration_minutes: Optional[int] = None) -> Dict:
        """Search for YouTube yoga videos"""
        try:
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "key": self.youtube_api_key,
                "q": query,
                "part": "snippet",
                "type": "video",
                "maxResults": 1,
                "videoCategoryId": "26"  # Howto & Style
            }
            
            if duration_minutes:
                if duration_minutes <= 15:
                    params["videoDuration"] = "short"
                elif duration_minutes <= 30:
                    params["videoDuration"] = "medium"
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("items") and len(data["items"]) > 0:
                    video = data["items"][0]
                    video_id = video["id"]["videoId"]
                    snippet = video["snippet"]
                    
                    return {
                        "success": True,
                        "video_id": video_id,
                        "title": snippet["title"],
                        "description": snippet.get("description", "")[:200],
                        "thumbnail": snippet["thumbnails"]["default"]["url"],
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "channel": snippet["channelTitle"]
                    }
            
            return {"success": False, "error": "No videos found"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_yoga_plan(self, user_id: int, session_type: str, duration_minutes: int,
                          energy_trend: str, stress_level: int, yoga_experience: str) -> YogaPlan:
        """Generate a yoga plan with YouTube video"""
        
        # Build search query based on session type and parameters
        query_parts = ["yoga"]
        
        if session_type == "stress_relief":
            query_parts.extend(["stress relief", "meditation", "gentle"])
        elif session_type == "energizing":
            query_parts.extend(["energizing", "morning", "vinyasa"])
        elif session_type == "flexibility":
            query_parts.extend(["flexibility", "stretching"])
        elif session_type == "strength":
            query_parts.extend(["strength", "power yoga"])
        elif session_type == "recovery":
            query_parts.extend(["restorative", "yin yoga", "recovery"])
        else:
            query_parts.append("beginner" if yoga_experience == "beginner" else "intermediate")
        
        if duration_minutes:
            query_parts.append(f"{duration_minutes} minutes")
        
        query = " ".join(query_parts)
        
        # Search for video
        video_result = self.search_youtube_video(query, duration_minutes)
        
        if not video_result.get("success"):
            # Fallback video
            video_result = {
                "success": True,
                "video_id": "dQw4w9WgXcQ",  # Placeholder
                "title": f"{session_type.title()} Yoga Session",
                "description": f"A {duration_minutes}-minute {session_type} yoga session",
                "url": f"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "thumbnail": "",
                "channel": "Yoga Wellness"
            }
        
        # Generate description
        description = self._generate_session_description(session_type, duration_minutes, energy_trend, stress_level)
        
        plan = YogaPlan(
            user_id=user_id,
            date=datetime.utcnow(),
            session_type=session_type,
            duration_minutes=duration_minutes,
            youtube_video_id=video_result["video_id"],
            youtube_title=video_result["title"],
            youtube_url=video_result["url"],
            description=description,
            created_by_agent="YogaAgent"
        )
        
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        
        return plan
    
    def _generate_session_description(self, session_type: str, duration_minutes: int,
                                     energy_trend: str, stress_level: int) -> str:
        """Generate session description"""
        descriptions = {
            "stress_relief": f"A gentle {duration_minutes}-minute session focused on stress relief, deep breathing, and relaxation. Perfect for calming the mind and body.",
            "energizing": f"An energizing {duration_minutes}-minute flow to boost your energy and motivation. Great for morning practice.",
            "flexibility": f"A {duration_minutes}-minute flexibility-focused session to improve range of motion and reduce stiffness.",
            "strength": f"A {duration_minutes}-minute strength-building session to build core stability and muscular endurance.",
            "recovery": f"A restorative {duration_minutes}-minute recovery session with gentle stretches and relaxation poses.",
        }
        
        return descriptions.get(session_type, f"A {duration_minutes}-minute balanced yoga session.")
    
    def generate_weekly_plan(self, user_id: int, recommendations: Dict, 
                            yoga_experience: str) -> List[YogaPlan]:
        """Generate a weekly yoga plan"""
        weekly_sessions = [
            {"day": "Monday", "type": "energizing", "duration": 30},
            {"day": "Tuesday", "type": "strength", "duration": 25},
            {"day": "Wednesday", "type": "flexibility", "duration": 20},
            {"day": "Thursday", "type": "stress_relief", "duration": 30},
            {"day": "Friday", "type": "energizing", "duration": 25},
            {"day": "Saturday", "type": "recovery", "duration": 40},
            {"day": "Sunday", "type": "stress_relief", "duration": 35},
        ]
        
        plans = []
        for session in weekly_sessions:
            plan = self.generate_yoga_plan(
                user_id=user_id,
                session_type=session["type"],
                duration_minutes=session["duration"],
                energy_trend=recommendations.get("energy_trend", "medium"),
                stress_level=recommendations.get("stress_level", 50),
                yoga_experience=yoga_experience
            )
            plans.append(plan)
        
        return plans

