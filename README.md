# 💰 Finance Tracker AI

> A full-stack AI-powered personal finance tracker built with Python FastAPI + Claude AI

![Python](https://img.shields.io/badge/Python-3.8+-ff4500?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688?style=flat-square&logo=fastapi&logoColor=white)
![Claude AI](https://img.shields.io/badge/Claude_AI-Anthropic-7F77DD?style=flat-square)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-BA7517?style=flat-square)
![Status](https://img.shields.io/badge/Status-WIP_🚧-ff4500?style=flat-square)

---

## ✨ Features

- 💰 **Track** income & expenses with categories
- 📊 **Budget** alerts when spending exceeds limits
- 🤖 **AI Advisor** powered by Claude AI for financial insights
- 📈 **Analytics** dashboard with spending trends
- 📁 **Export** monthly/weekly reports to CSV
- 🔐 **JWT Auth** with secure login/register

---

## 🗂️ Project Structure

```
finance-tracker/
├── backend/
│   ├── main.py          # FastAPI app & all routes
│   ├── config.py        # Settings & .env loader
│   ├── database.py      # SQLite + SQLAlchemy setup
│   ├── models.py        # DB models
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # JWT authentication
│   ├── transaction.py   # Transaction CRUD
│   ├── budget.py        # Budget logic
│   ├── analytics.py     # Spending analytics
│   ├── ai_advisor.py    # Claude AI integration
│   ├── reports.py       # CSV report generation
│   ├── validator.py     # Input validation
│   ├── logger.py        # Logging setup
│   ├── utils.py         # Helper functions
│   └── requirements.txt
├── frontend/
│   ├── index.html       # Login/Register page
│   ├── dashboard.html   # Main app dashboard
│   └── assets/
│       ├── style.css
│       └── app.js
├── .env.example
└── README.md
```

---

## 🚀 Setup & Run

**1. Clone the repo**
```bash
git clone https://github.com/ashish7802/finance-tracker-ai.git
cd finance-tracker-ai/backend
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment**
```bash
cp ../.env.example .env
# Edit .env and add your API keys
```

**4. Run backend**
```bash
uvicorn main:app --reload
```

**5. Open frontend** (new terminal)
```bash
cd ../frontend
python -m http.server 5500
# Visit: http://localhost:5500
```

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Claude AI API key from Anthropic |
| `JWT_SECRET` | Secret key for signing JWT tokens |
| `DATABASE_URL` | SQLite URL (default: `sqlite:///./finance.db`) |

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Create new account |
| POST | `/auth/login` | Login & get JWT token |

### Transactions
| Method | Endpoint | Description |
|---|---|---|
| GET | `/transactions` | List all transactions |
| POST | `/transactions` | Add new transaction |
| PUT | `/transactions/{id}` | Update transaction |
| DELETE | `/transactions/{id}` | Delete transaction |
| GET | `/transactions/search?q=` | Search transactions |

### Budgets
| Method | Endpoint | Description |
|---|---|---|
| GET | `/budgets` | List all budgets |
| POST | `/budgets` | Set budget for category |
| GET | `/budgets/status` | Budget vs actual spending |

### Analytics
| Method | Endpoint | Description |
|---|---|---|
| GET | `/analytics/summary` | Income, expense, savings |
| GET | `/analytics/by-category` | Spending per category |
| GET | `/analytics/monthly-trend` | Month wise trends |
| GET | `/analytics/top-expenses` | Biggest expense categories |

### AI Advisor
| Method | Endpoint | Description |
|---|---|---|
| POST | `/ai/advice` | Get AI financial advice |
| POST | `/ai/question` | Ask AI a custom question |

### Reports
| Method | Endpoint | Description |
|---|---|---|
| GET | `/reports/weekly` | Weekly summary |
| GET | `/reports/monthly` | Monthly summary |
| GET | `/reports/export-csv` | Download CSV report |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + FastAPI |
| Database | SQLite + SQLAlchemy |
| Auth | JWT + bcrypt |
| AI | Anthropic Claude API |
| Frontend | Vanilla HTML + CSS + JS |

---

## 👨‍💻 Author

**Ashish Yadav** — [@ashish7802](https://github.com/ashish7802)

⭐ Star this repo if you find it useful!
