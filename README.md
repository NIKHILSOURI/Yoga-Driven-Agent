### *Yoga-Driven Agentic Wellness & Nutrition Coach

**Innov-AI-tion Challenge Submission**  
**Problem Domain:** *Agentic Systems for Healthcare & Fitness*

A next-generation **multi-agent, neuro-symbolic, goal-driven wellness system** that behaves like an **autonomous health coach** rather than a static chatbot.

It follows the agentic loop:  
**Observe → Reason → Plan → Act → Reflect → Replan**,  
using **symbolic wellness rules, lightweight ML predictions, memory retrieval, and external tool/API interaction**.

> ⚠ **Safety Scope:** Wellness only — **No medical diagnosis, No treatment advice**.  
> Designed for **holistic fitness, yoga-synergy nutrition (Sattvic diet), stress tracking, and habit coaching**.

---

## ❗ Innov-AI-tion Problem Statement (Aligned)

Fitness & healthcare apps today:
- provide **static plans**
- lack **reasoning transparency**
- fail to adapt based on **daily constraints**
- don't interact intelligently with **tools or feedback**
- lack **long-term goal autonomy**

### Our system solves this by demonstrating true agentic capabilities:
✔ Goal-oriented behavior  
✔ Multi-step planning  
✔ Autonomous decisions under constraints  
✔ Tool interaction (Food & Video APIs)  
✔ Memory-driven personalization  
✔ Transparent decision traces  

---

## 🎯 Objective

Build an agentic system that:
- generates **personalized daily/weekly yoga sessions**
- produces **nutrient-balanced meal plans**
- substitutes meals using **memory of dislikes/likes**
- adapts intensity using **ML fatigue/appetite prediction**
- interacts with **external free-tier APIs**
- shows **why** each plan was chosen

---

## 🧠 Multi-Agent Roles

| Agent | Role |
|---|---|
| **Observe Agent** | Collects & validates check-ins (sleep, mood, appetite, ingredients, quiz, adherence) |
| **Reasoner Agent (NSMR Core)** | Applies symbolic wellness rules + constraints, queries memory, receives ML predictions |
| **Nutrition Agent** | Calls USDA API, generates Sattvic meals, swaps ingredients, creates recipes via LLM |
| **Yoga Agent** | Generates yoga plans & calls YouTube API for personalized video suggestions |
| **Fairness Agent** | Prevents API quota bias and ensures fair tool usage for all users |
| **Report Agent** | Generates weekly/monthly summaries & insights |
| **ML Predictor** | Fatigue & Appetite classification (low/medium/high), influences plan intensity |

---

## 🧩 Constraints Used by Agents

- sleep < 5h → short yoga session
- low energy → warm, easy-to-cook meals
- disliked food/video → avoid repetition via memory
- BYHOUR constraint on scheduling (calendar-ready mode)
- API quotas are monitored by **Fairness Agent**
- Dataset must be **public or synthetic**

---

## 🏗 System Architecture

### **Backend:** FastAPI + SQLite + SQLAlchemy + Multi-Agent Core  
### **Frontend:** Next.js 14 + TypeScript + Tailwind CSS + Recharts  
### **APIs Used (Free Tier):**
- **OpenAI** → Recipes, Coach Chat, Decision Explanation
- **USDA FoodData Central** → Nutrient Lookup
- **YouTube Data API** → Yoga & Meditation Videos
- **Google Calendar** → Optional Scheduling (not required, but ready)

---

## 📁 Repository Structure

```
NSMR-Health-Coach/
├── backend/
│   ├── agents/
│   ├── routers/
│   ├── database.py
│   ├── main.py
│   └── wellness.db (auto-created)
├── frontend/
│   ├── app/
│   ├── components/
│   └── lib/api.ts
├── demo/DecisionTraceViewer.mp4
├── .env (API keys — not hardcoded)
└── README.md
```


## 🚀 Run the System

### Backend

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Access URLs

- **Frontend** → http://localhost:3000
- **Backend API** → http://localhost:8000
- **API Docs** → http://localhost:8000/docs

## 📊 Expected Outputs

| Component | Output |
|-----------|--------|
| Daily Plan | Personalized meals + yoga session |
| ML Predictor | Fatigue/Appetite classification |
| Nutrition Agent | Nutrient breakdown + recipe |
| Yoga Agent | YouTube video suggestions |
| Reasoner | Human-readable explanation |
| Fairness Agent | Quota-balanced API usage |
| Decision Trace | Triggered rules + memory + API calls |
| Reports | Weekly/Monthly progress summaries |

## ⚖️ Ethics & Limitations

- **Wellness system only** (not medical)
- **No diagnosis or treatment suggestions**
- **Depends on free-tier API reliability**
- **ML model needs larger data** for stronger generalization
- **Personalization depends on honest check-ins**
- **API quota bias prevented** using Fairness agent

## 🔮 Future Scope

- **Wearable integration** (sleep, HR, steps, calories)
- **Google Calendar scheduling** + reminders
- **Group wellness challenges** with shared resource fairness
- **Improved ML training** with cross-dataset generalization
- **Expanded multilingual support** (Telugu, Hindi, English)
- **Recipe image generation** & difficulty index scoring

## 🧑‍🎓 Signature

**Yalamati Nikhil Souri**  
Final Year BTech (CSE) • JNTUACEA, Anantapur, India  
B.Sc. Computer Science • Blekinge Institute of Technology, Karlskrona, Sweden  
GitHub: [NIKHILSOURI](https://github.com/NIKHILSOURI) • [NIKHILSOURI360](https://github.com/NIKHILSOURI360)
