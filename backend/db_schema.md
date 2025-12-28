# Database Schema Documentation

## Overview

The database uses SQLite by default (can be changed to PostgreSQL/MySQL via DATABASE_URL). All tables are automatically created on server startup via `init_db()`.

## Tables

### 1. `users`
User profile information.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| email | String | Unique email address |
| name | String | User's name |
| age | Integer | User's age |
| gender | String | Gender (male/female/other) |
| yoga_experience | String | beginner/intermediate/advanced |
| dietary_preferences | JSON | List of dietary preferences |
| allergies | JSON | List of allergies |
| goals | JSON | List of wellness goals |
| activity_level | String | Activity level |
| created_at | DateTime | Account creation timestamp |

### 2. `checkins`
Daily check-in data.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users |
| date | DateTime | Check-in date |
| mood | String | Mood (happy/neutral/sad/stressed) |
| mood_score | Integer | Mood score 1-10 |
| appetite | Float | Appetite level 0-10 |
| energy | Float | Energy level 0-10 |
| sleep_hours | Float | Hours of sleep |
| adherence | Float | Plan adherence 0-100% |
| ingredients | Text | Available ingredients (comma-separated) |
| notes | Text | Additional notes |

### 3. `quiz_responses`
Mental health quiz responses.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users |
| date | DateTime | Quiz completion date |
| stress_score | Integer | Stress score 1-10 |
| anxiety_score | Integer | Anxiety score 1-10 |
| motivation_score | Integer | Motivation score 1-10 |
| mindfulness_score | Integer | Mindfulness score 1-10 |
| appetite_indicator | Integer | Appetite indicator 1-10 |
| sleep_quality | Integer | Sleep quality 1-10 |
| total_score | Integer | Average score |
| responses | JSON | Full response data |

### 4. `nutrition_plans`
Generated nutrition/meal plans.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users |
| date | DateTime | Plan creation date |
| meal_type | String | breakfast/lunch/dinner/snack |
| recipe_name | String | Name of the recipe |
| ingredients | JSON | List of ingredients |
| nutrients | JSON | Nutrient data (calories, protein, fiber, etc.) |
| recipe_instructions | Text | Cooking instructions |
| meal_simplicity_index | Float | Ease of preparation 1-10 |
| sattvic_score | Float | Sattvic alignment score 1-10 |
| created_by_agent | String | Which agent created this |

### 5. `yoga_plans`
Generated yoga practice plans.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users |
| date | DateTime | Plan creation date |
| session_type | String | flexibility/strength/stress_relief/recovery |
| duration_minutes | Integer | Session duration |
| youtube_video_id | String | YouTube video ID |
| youtube_title | String | Video title |
| youtube_url | String | Full YouTube URL |
| description | Text | Session description |
| created_by_agent | String | Which agent created this |

### 6. `ml_predictions`
ML model predictions.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users |
| date | DateTime | Prediction date |
| energy_trend | String | low/medium/high |
| appetite_trend | String | low/normal/high |
| input_features | JSON | Input features used |
| prediction_confidence | Float | Confidence score 0-1 |

### 7. `decision_traces`
AI decision traces for transparency.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users |
| date | DateTime | Decision timestamp |
| agent_name | String | Which agent made the decision |
| triggered_rules | JSON | Rules that were triggered |
| memory_retrieved | JSON | Memory items retrieved |
| plan_chosen | JSON | Plan that was chosen |
| tools_called | JSON | External tools used |
| explanation | Text | Human-readable explanation |

### 8. `progress`
Progress tracking data.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users |
| date | DateTime | Progress date |
| yoga_streak | Integer | Consecutive yoga days |
| consistency_percentage | Float | Consistency percentage |
| protein_total | Float | Total protein intake |
| fiber_total | Float | Total fiber intake |
| calcium_total | Float | Total calcium intake |
| stress_reduction | Float | Stress reduction percentage |
| adherence_improvement | Float | Adherence improvement |

### 9. `memory`
Memory system for preferences and patterns.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users |
| memory_type | String | preference/successful_plan/disliked_meal/api_call_* |
| content | JSON | Memory content |
| created_at | DateTime | Creation timestamp |
| last_accessed | DateTime | Last access timestamp |

## Relationships

- `users` (1) → (many) `checkins`
- `users` (1) → (many) `quiz_responses`
- `users` (1) → (many) `nutrition_plans`
- `users` (1) → (many) `yoga_plans`
- `users` (1) → (many) `ml_predictions`
- `users` (1) → (many) `decision_traces`
- `users` (1) → (many) `progress`
- `users` (1) → (many) `memory`

## Indexes

- `users.email` - Unique index for fast lookups
- `user_id` - Indexed on all foreign key columns for performance

## Database Location

By default, the database file is created at: `backend/wellness.db`

To change the database location, update `DATABASE_URL` in `.env`:
- SQLite: `sqlite:///./path/to/database.db`
- PostgreSQL: `postgresql://user:password@localhost/dbname`
- MySQL: `mysql://user:password@localhost/dbname`

## Backup

To backup the SQLite database:
```bash
cp wellness.db wellness_backup.db
```

## Reset Database

To reset the database (⚠️ deletes all data):
```bash
python db_init.py --reset
```

