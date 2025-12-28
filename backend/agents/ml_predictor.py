import numpy as np
from typing import Dict, Tuple
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

class FatigueAppetitePredictor:
    """Lightweight ML model for predicting energy and appetite trends"""
    
    def __init__(self):
        self.energy_model = None
        self.appetite_model = None
        self.model_path = "models"
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize or load models"""
        os.makedirs(self.model_path, exist_ok=True)
        
        # Simple rule-based model for hackathon (can be replaced with trained model)
        # In production, this would load a pre-trained model
        self.energy_model = self._create_rule_based_energy_model()
        self.appetite_model = self._create_rule_based_appetite_model()
    
    def _create_rule_based_energy_model(self):
        """Rule-based energy predictor"""
        def predict(sleep, mood, adherence, stress, motivation, day_type):
            score = 0
            # Sleep contribution (0-3)
            if sleep >= 8:
                score += 3
            elif sleep >= 6:
                score += 2
            else:
                score += 1
            
            # Mood contribution (0-2)
            if mood >= 7:
                score += 2
            elif mood >= 4:
                score += 1
            
            # Adherence contribution (0-2)
            if adherence >= 70:
                score += 2
            elif adherence >= 40:
                score += 1
            
            # Stress negative (0 to -2)
            if stress >= 70:
                score -= 2
            elif stress >= 50:
                score -= 1
            
            # Motivation (0-1)
            if motivation >= 60:
                score += 1
            
            # Day type
            if day_type == "weekend":
                score += 1
            
            if score >= 6:
                return "high"
            elif score >= 3:
                return "medium"
            else:
                return "low"
        
        return predict
    
    def _create_rule_based_appetite_model(self):
        """Rule-based appetite predictor"""
        def predict(sleep, mood, adherence, stress, energy, day_type):
            score = 0
            # Sleep contribution
            if sleep >= 7:
                score += 2
            elif sleep >= 5:
                score += 1
            
            # Mood contribution
            if mood >= 6:
                score += 2
            elif mood >= 4:
                score += 1
            
            # Stress negative
            if stress >= 70:
                score -= 2
            elif stress >= 50:
                score -= 1
            
            # Energy positive
            if energy >= 7:
                score += 1
            
            if score >= 4:
                return "high"
            elif score >= 2:
                return "normal"
            else:
                return "low"
        
        return predict
    
    def predict(self, features: Dict) -> Tuple[str, str, float]:
        """
        Predicts energy and appetite trends
        Returns: (energy_trend, appetite_trend, confidence)
        """
        sleep = features.get("sleep_hours", 7.0)
        mood = features.get("mood_score", 5)
        adherence = features.get("adherence_avg", 50.0)
        stress = features.get("stress_score", 50)
        motivation = features.get("motivation_score", 50)
        energy = features.get("energy", 5.0)
        day_type = features.get("day_type", "weekday")
        
        energy_trend = self.energy_model(sleep, mood, adherence, stress, motivation, day_type)
        appetite_trend = self.appetite_model(sleep, mood, adherence, stress, energy, day_type)
        
        # Simple confidence calculation
        confidence = 0.75  # Can be made more sophisticated
        
        return energy_trend, appetite_trend, confidence

