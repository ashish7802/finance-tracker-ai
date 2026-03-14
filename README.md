# Finance Tracker (FastAPI + Vanilla JS)

A full-stack finance tracker web app where business logic is handled in Python (FastAPI), with minimal HTML/CSS/JS for UI and API calls.

## Project Structure

```
finance-tracker/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── transaction.py
│   ├── budget.py
│   ├── analytics.py
│   ├── ai_advisor.py
│   ├── reports.py
│   ├── validator.py
│   ├── logger.py
│   ├── utils.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   └── assets/
│       ├── style.css
│       └── app.js
├── .env.example
└── README.md
```

## Setup

1. Create virtual env and install deps:
   ```bash
   cd finance-tracker/backend
   pip install -r requirements.txt
   ```
2. Configure environment variables:
   ```bash
   cp ../.env.example .env
   ```
3. Run backend:
   ```bash
   uvicorn main:app --reload
   ```
4. Open frontend:
   ```bash
   cd ../frontend
   python -m http.server 5500
   ```

## Environment Variables

- `ANTHROPIC_API_KEY`: Anthropic API key for AI advisor endpoints.
- `JWT_SECRET`: Secret used to sign JWTs.
- `DATABASE_URL`: SQLite database URL (default: `sqlite:///./finance.db`).

## API Endpoints

### Auth
- `POST /auth/register`
- `POST /auth/login`

### Transactions
- `GET /transactions`
- `POST /transactions`
- `PUT /transactions/{id}`
- `DELETE /transactions/{id}`
- `GET /transactions/search?q=`

### Budgets
- `GET /budgets`
- `POST /budgets`
- `GET /budgets/status`

### Analytics
- `GET /analytics/summary`
- `GET /analytics/by-category`
- `GET /analytics/monthly-trend`
- `GET /analytics/top-expenses`

### AI Advisor
- `POST /ai/advice`
- `POST /ai/question`

### Reports
- `GET /reports/weekly`
- `GET /reports/monthly`
- `GET /reports/export-csv`
