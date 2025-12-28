from typing import Dict, List
from sqlalchemy.orm import Session
from database import Memory
from datetime import datetime, timedelta

class FairnessAgent:
    """Ensures fair API free-tier usage and prevents quota bias"""
    
    def __init__(self, db: Session):
        self.db = db
        self.api_call_limits = {
            "usda": {"daily": 100, "per_user_daily": 10},
            "youtube": {"daily": 100, "per_user_daily": 10},
            "openai": {"daily": 50, "per_user_daily": 5},
        }
    
    def check_api_quota(self, api_name: str, user_id: int) -> Dict:
        """Check if API call is allowed"""
        today = datetime.utcnow().date()
        
        # In a real system, track API calls in a separate table
        # For now, use memory system to track
        recent_calls = self.db.query(Memory).filter(
            Memory.user_id == user_id,
            Memory.memory_type == f"api_call_{api_name}",
            Memory.created_at >= datetime.combine(today, datetime.min.time())
        ).count()
        
        limit = self.api_call_limits.get(api_name, {}).get("per_user_daily", 10)
        
        if recent_calls >= limit:
            return {
                "allowed": False,
                "reason": f"Daily limit reached for {api_name}",
                "calls_used": recent_calls,
                "limit": limit
            }
        
        return {
            "allowed": True,
            "calls_used": recent_calls,
            "limit": limit,
            "remaining": limit - recent_calls
        }
    
    def record_api_call(self, api_name: str, user_id: int):
        """Record an API call"""
        memory = Memory(
            user_id=user_id,
            memory_type=f"api_call_{api_name}",
            content={"timestamp": datetime.utcnow().isoformat()},
            created_at=datetime.utcnow(),
            last_accessed=datetime.utcnow()
        )
        self.db.add(memory)
        self.db.commit()
    
    def ensure_fair_distribution(self, user_ids: List[int], resource: str) -> bool:
        """Ensure fair distribution of resources across users"""
        # Simple fairness check - ensure no single user dominates
        today = datetime.utcnow().date()
        
        user_call_counts = {}
        for user_id in user_ids:
            count = self.db.query(Memory).filter(
                Memory.user_id == user_id,
                Memory.memory_type == f"api_call_{resource}",
                Memory.created_at >= datetime.combine(today, datetime.min.time())
            ).count()
            user_call_counts[user_id] = count
        
        if user_call_counts:
            max_calls = max(user_call_counts.values())
            min_calls = min(user_call_counts.values())
            
            # If disparity is too large, prioritize users with fewer calls
            if max_calls - min_calls > 5:
                return False  # Unfair distribution detected
        
        return True

