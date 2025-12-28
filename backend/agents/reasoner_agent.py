from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from database import DecisionTrace, Memory
from .ml_predictor import FatigueAppetitePredictor
from .observe_agent import ObserveAgent
from datetime import datetime

class ReasonerAgent:
    """NSMR Core: Applies symbolic wellness rules + ML predictions to select plans"""
    
    def __init__(self, db: Session):
        self.db = db
        self.ml_predictor = FatigueAppetitePredictor()
        self.observe_agent = ObserveAgent(db)
    
    def reason(self, user_id: int) -> Dict:
        """Main reasoning function"""
        # Observe
        observed_data = self.observe_agent.collect_daily_data(user_id)
        
        # Predict
        ml_features = {
            "sleep_hours": observed_data["checkin"]["sleep_hours"],
            "mood_score": observed_data["checkin"]["mood_score"],
            "adherence_avg": observed_data["adherence"]["last_3_days_avg"],
            "stress_score": observed_data["quiz"]["stress_score"],
            "motivation_score": observed_data["quiz"]["motivation_score"],
            "energy": observed_data["checkin"]["energy"],
            "day_type": observed_data["day_type"],
        }
        
        energy_trend, appetite_trend, confidence = self.ml_predictor.predict(ml_features)
        
        # Apply symbolic rules
        rules_triggered = self._apply_wellness_rules(observed_data, energy_trend, appetite_trend)
        
        # Retrieve relevant memory
        memory_retrieved = self._retrieve_memory(user_id, observed_data)
        
        # Generate plan recommendations
        plan_recommendations = self._generate_recommendations(
            observed_data, energy_trend, appetite_trend, rules_triggered, memory_retrieved
        )
        
        # Store decision trace
        trace = DecisionTrace(
            user_id=user_id,
            date=datetime.utcnow(),
            agent_name="ReasonerAgent",
            triggered_rules=rules_triggered,
            memory_retrieved=memory_retrieved,
            plan_chosen=plan_recommendations,
            tools_called={"ml_predictor": True},
            explanation=self._generate_explanation(rules_triggered, energy_trend, appetite_trend)
        )
        self.db.add(trace)
        self.db.commit()
        
        return {
            "energy_trend": energy_trend,
            "appetite_trend": appetite_trend,
            "confidence": confidence,
            "rules_triggered": rules_triggered,
            "memory_retrieved": memory_retrieved,
            "recommendations": plan_recommendations,
            "explanation": trace.explanation,
        }
    
    def _apply_wellness_rules(self, data: Dict, energy_trend: str, appetite_trend: str) -> List[Dict]:
        """Apply symbolic wellness rules"""
        rules = []
        
        stress = data["quiz"]["stress_score"]
        motivation = data["quiz"]["motivation_score"]
        sleep = data["checkin"]["sleep_hours"]
        adherence = data["adherence"]["last_3_days_avg"]
        
        # Rule 1: High stress → gentle yoga + meditation + magnesium food
        if stress > 80:
            rules.append({
                "rule_id": "high_stress_relief",
                "condition": f"stress_score > 80 ({stress})",
                "action": "gentle_yoga_meditation_magnesium",
                "priority": "high"
            })
        
        # Rule 2: Low motivation → energizing yoga + favorite meal reward
        if motivation < 40:
            rules.append({
                "rule_id": "low_motivation_boost",
                "condition": f"motivation_score < 40 ({motivation})",
                "action": "energizing_yoga_favorite_meal",
                "priority": "high"
            })
        
        # Rule 3: Low energy → shorter gentle yoga + warm simple meals
        if energy_trend == "low":
            rules.append({
                "rule_id": "low_energy_gentle",
                "condition": f"energy_trend = low",
                "action": "gentle_yoga_warm_meals",
                "priority": "medium"
            })
        
        # Rule 4: Low appetite → nutrient-dense smaller portions
        if appetite_trend == "low":
            rules.append({
                "rule_id": "low_appetite_nutrient_dense",
                "condition": f"appetite_trend = low",
                "action": "nutrient_dense_small_portions",
                "priority": "medium"
            })
        
        # Rule 5: Poor adherence → simplified plans
        if adherence < 40:
            rules.append({
                "rule_id": "poor_adherence_simplify",
                "condition": f"adherence < 40% ({adherence:.1f}%)",
                "action": "simplified_plans",
                "priority": "high"
            })
        
        # Rule 6: Low sleep → recovery focus
        if sleep < 6:
            rules.append({
                "rule_id": "low_sleep_recovery",
                "condition": f"sleep < 6 hours ({sleep})",
                "action": "recovery_yoga_restorative_meals",
                "priority": "medium"
            })
        
        return rules
    
    def _retrieve_memory(self, user_id: int, data: Dict) -> List[Dict]:
        """Retrieve relevant memories"""
        memories = self.db.query(Memory).filter(
            Memory.user_id == user_id
        ).order_by(Memory.last_accessed.desc()).limit(5).all()
        
        return [{
            "type": m.memory_type,
            "content": m.content,
            "last_accessed": m.last_accessed.isoformat() if m.last_accessed else None
        } for m in memories]
    
    def _generate_recommendations(self, data: Dict, energy_trend: str, appetite_trend: str, 
                                 rules: List[Dict], memory: List[Dict]) -> Dict:
        """Generate plan recommendations"""
        recommendations = {
            "yoga": {
                "session_type": "balanced",
                "duration_minutes": 30,
                "intensity": "medium",
            },
            "nutrition": {
                "meal_complexity": "medium",
                "focus": "balanced_sattvic",
                "portion_size": "normal",
            },
            "special_actions": [],
        }
        
        # Apply rule-based modifications
        for rule in rules:
            if rule["rule_id"] == "high_stress_relief":
                recommendations["yoga"]["session_type"] = "stress_relief"
                recommendations["yoga"]["intensity"] = "gentle"
                recommendations["nutrition"]["focus"] = "magnesium_rich"
                recommendations["special_actions"].append("meditation_session")
            
            elif rule["rule_id"] == "low_motivation_boost":
                recommendations["yoga"]["session_type"] = "energizing"
                recommendations["yoga"]["intensity"] = "moderate"
                recommendations["nutrition"]["focus"] = "favorite_meal"
                recommendations["special_actions"].append("reward_meal")
            
            elif rule["rule_id"] == "low_energy_gentle":
                recommendations["yoga"]["duration_minutes"] = 15
                recommendations["yoga"]["intensity"] = "gentle"
                recommendations["nutrition"]["meal_complexity"] = "simple"
                recommendations["nutrition"]["focus"] = "warm_comforting"
            
            elif rule["rule_id"] == "low_appetite_nutrient_dense":
                recommendations["nutrition"]["portion_size"] = "small"
                recommendations["nutrition"]["focus"] = "nutrient_dense"
            
            elif rule["rule_id"] == "poor_adherence_simplify":
                recommendations["yoga"]["duration_minutes"] = 10
                recommendations["nutrition"]["meal_complexity"] = "simple"
                recommendations["special_actions"].append("simplified_mode")
        
        return recommendations
    
    def _generate_explanation(self, rules: List[Dict], energy_trend: str, appetite_trend: str) -> str:
        """Generate human-readable explanation"""
        explanation_parts = [
            f"Based on ML predictions: Energy trend is {energy_trend}, Appetite trend is {appetite_trend}."
        ]
        
        if rules:
            explanation_parts.append(f"Triggered {len(rules)} wellness rules:")
            for rule in rules[:3]:  # Top 3 rules
                explanation_parts.append(f"- {rule['rule_id']}: {rule['condition']} → {rule['action']}")
        else:
            explanation_parts.append("No special rules triggered. Using balanced default plan.")
        
        return " ".join(explanation_parts)

