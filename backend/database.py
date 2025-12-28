from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wellness.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User Profile
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    yoga_experience = Column(String)  # beginner, intermediate, advanced
    dietary_preferences = Column(JSON)  # vegetarian, vegan, etc.
    allergies = Column(JSON)
    goals = Column(JSON)  # weight_loss, muscle_gain, stress_relief, etc.
    activity_level = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Daily Check-in
class CheckIn(Base):
    __tablename__ = "checkins"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    mood = Column(String)  # happy, neutral, sad, stressed
    mood_score = Column(Integer)  # 1-10
    appetite = Column(Float)  # 0-10
    energy = Column(Float)  # 0-10
    sleep_hours = Column(Float)
    adherence = Column(Float)  # 0-100
    ingredients = Column(Text)  # comma-separated
    notes = Column(Text)

# Mental Health Quiz
class QuizResponse(Base):
    __tablename__ = "quiz_responses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    stress_score = Column(Integer)
    anxiety_score = Column(Integer)
    motivation_score = Column(Integer)
    mindfulness_score = Column(Integer)
    appetite_indicator = Column(Integer)
    sleep_quality = Column(Integer)
    total_score = Column(Integer)
    responses = Column(JSON)

# Nutrition Plans
class NutritionPlan(Base):
    __tablename__ = "nutrition_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    meal_type = Column(String)  # breakfast, lunch, dinner, snack
    recipe_name = Column(String)
    ingredients = Column(JSON)
    nutrients = Column(JSON)  # calories, protein, fiber, etc.
    recipe_instructions = Column(Text)
    meal_simplicity_index = Column(Float)
    sattvic_score = Column(Float)
    created_by_agent = Column(String)  # which agent created this

# Yoga Plans
class YogaPlan(Base):
    __tablename__ = "yoga_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    session_type = Column(String)  # flexibility, strength, stress_relief, recovery
    duration_minutes = Column(Integer)
    youtube_video_id = Column(String)
    youtube_title = Column(String)
    youtube_url = Column(String)
    description = Column(Text)
    created_by_agent = Column(String)

# ML Predictions
class MLPrediction(Base):
    __tablename__ = "ml_predictions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    energy_trend = Column(String)  # low, medium, high
    appetite_trend = Column(String)  # low, normal, high
    input_features = Column(JSON)
    prediction_confidence = Column(Float)

# Decision Traces
class DecisionTrace(Base):
    __tablename__ = "decision_traces"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    agent_name = Column(String)
    triggered_rules = Column(JSON)
    memory_retrieved = Column(JSON)
    plan_chosen = Column(JSON)
    tools_called = Column(JSON)
    explanation = Column(Text)

# Progress Tracking
class Progress(Base):
    __tablename__ = "progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    yoga_streak = Column(Integer)
    consistency_percentage = Column(Float)
    protein_total = Column(Float)
    fiber_total = Column(Float)
    calcium_total = Column(Float)
    stress_reduction = Column(Float)
    adherence_improvement = Column(Float)

# Memory System
class Memory(Base):
    __tablename__ = "memory"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    memory_type = Column(String)  # preference, successful_plan, disliked_meal, etc.
    content = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

