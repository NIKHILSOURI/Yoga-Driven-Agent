# Yoga Wellness Coach - Project Summary

## 🎯 Project Overview

A comprehensive SaaS-level **Agentic Wellness & Nutrition Coach** that generates personalized nutrition plans rooted in yoga philosophy (Sattvic nutrition) while adapting daily using ML predictions, symbolic rule reasoning, memory, and external tool interactions.

## ✨ Key Features Implemented

### 1. Multi-Agent System
- **Observe Agent**: Collects sleep, mood, ingredients, adherence, quiz scores
- **Reasoner Agent (NSMR Core)**: Applies symbolic wellness rules + ML predictions
- **Nutrition Agent**: Nutrient lookup, recipe generation, substitutions
- **Yoga Agent**: Daily/weekly yoga plans + YouTube video recommendations
- **Fairness Agent**: Ensures fair API usage and prevents quota bias
- **Report Agent**: Generates weekly & monthly progress summaries

### 2. ML Model
- **Fatigue & Appetite Predictor**: Lightweight, explainable model
- Predicts energy trends (low/medium/high) and appetite trends (low/normal/high)
- Influences yoga session intensity and meal planning

### 3. Professional Frontend
- **Dashboard**: Analytics, charts, progress tracking
- **Daily Check-in Panel**: Mood, energy, sleep, adherence tracking
- **Chatbot Interface**: AI-powered wellness coach conversations
- **Decision Trace Viewer**: Transparent AI decision-making process
- **Mental Health Quiz**: Non-clinical wellness assessment
- **Onboarding**: User profile setup

### 4. API Integrations
- ✅ **OpenAI**: Recipe generation and chatbot
- ✅ **USDA FoodData Central**: Nutrient lookup
- ✅ **YouTube Data API**: Yoga video recommendations
- ✅ **Google Calendar API**: Ready for scheduling (optional)

### 5. Database & Memory System
- SQLite database with SQLAlchemy ORM
- Stores user profiles, check-ins, plans, quiz responses
- Memory system for preferences and successful plans
- Decision trace logging for transparency

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── agents/           # Multi-agent system
│   ├── observe_agent.py
│   ├── reasoner_agent.py
│   ├── nutrition_agent.py
│   ├── yoga_agent.py
│   ├── fairness_agent.py
│   ├── report_agent.py
│   └── ml_predictor.py
├── routers/          # API endpoints
│   ├── auth.py
│   ├── profile.py
│   ├── checkin.py
│   ├── nutrition.py
│   ├── yoga.py
│   ├── quiz.py
│   ├── dashboard.py
│   ├── reports.py
│   ├── chatbot.py
│   └── trace.py
├── database.py       # Database models
└── main.py          # FastAPI app
```

### Frontend (Next.js 14)
```
frontend/
├── app/              # Next.js app directory
│   ├── page.tsx     # Main page
│   ├── layout.tsx
│   └── globals.css
├── components/      # React components
│   ├── Dashboard.tsx
│   ├── CheckInPanel.tsx
│   ├── Chatbot.tsx
│   ├── DecisionTrace.tsx
│   ├── MentalHealthQuiz.tsx
│   ├── Navigation.tsx
│   └── Onboarding.tsx
└── lib/
    └── api.ts       # API client
```

## 🔄 Agentic Loop

The system follows the **Observe → Reason → Plan → Act → Reflect → Replan** loop:

1. **Observe**: Collects daily check-in data, quiz scores, past adherence
2. **Reason**: ML predictions + symbolic rules → generates recommendations
3. **Plan**: Creates nutrition and yoga plans based on reasoning
4. **Act**: User follows plans
5. **Reflect**: Tracks adherence and outcomes
6. **Replan**: Adapts next day's plans based on results

## 📊 Decision Transparency

Every decision is logged with:
- Triggered symbolic rules
- Memory retrieved (past preferences/successes)
- ML predictions used
- External tools called
- Human-readable explanation

## 🎨 UI Highlights

- **Modern Design**: Gradient backgrounds, card-based layout, smooth animations
- **Interactive Charts**: Recharts for data visualization
- **Responsive**: Works on desktop and mobile
- **Professional**: SaaS-level polish with consistent color scheme
- **User-Friendly**: Clear navigation, intuitive forms, helpful feedback

## 🔐 API Keys Configuration

All API keys are stored in `backend/.env`:
- OpenAI API Key
- USDA FoodData Central API Key
- YouTube Data API Key
- Google Calendar API Key (optional)

## 🚀 Getting Started

1. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   # Create .env with API keys
   uvicorn main:app --reload
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Access**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 📝 Key Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/checkin/{user_id}` - Submit daily check-in
- `GET /api/dashboard/{user_id}/overview` - Dashboard data
- `POST /api/chatbot/chat` - Chat with wellness coach
- `GET /api/trace/{user_id}/today` - Decision traces
- `POST /api/quiz/{user_id}` - Submit mental health quiz
- `GET /api/reports/weekly/{user_id}` - Weekly report

## ⚠️ Ethics & Limitations

- **Wellness System Only**: Not a medical system
- **No Diagnosis**: No medical diagnosis or treatment recommendations
- **Non-Clinical**: Mental health quiz is for wellness tracking only
- **API Dependent**: Nutrient data depends on free-tier API accuracy
- **User Honesty**: Plans rely on accurate user check-ins

## 🎯 Novelty Highlights

1. **Yoga-Nutrition Synergy**: Rare combination in fitness apps
2. **Agentic Loop**: Transparent decision-making process
3. **ML-Driven Adaptation**: Fatigue & appetite prediction influences plans
4. **Memory System**: Avoids repetition, improves adherence
5. **Fairness Agent**: Ensures unbiased plan selection
6. **Decision Transparency**: Every decision is traceable
7. **Sattvic Nutrition**: Yoga-aligned meal planning

## 📈 Future Enhancements

- Wearable data integration (HR, steps)
- Google Calendar scheduling
- Multi-language support (Telugu/Hindi/English)
- Advanced ML model training
- Recipe image generation
- Social features (sharing plans)

## 🏆 Hackathon Ready

This project is fully functional and ready for hackathon submission with:
- ✅ Complete backend API
- ✅ Professional frontend UI
- ✅ All required features implemented
- ✅ API integrations working
- ✅ Documentation complete
- ✅ Transparent decision-making
- ✅ Ethics considerations addressed

