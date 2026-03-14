from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import analytics
import budget
import models
import reports
import schemas
import transaction
from ai_advisor import answer_question, get_advice
from auth import create_access_token, get_current_user, hash_password, verify_password
from database import Base, engine, get_db
from logger import setup_logger

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Tracker API")
logger = setup_logger()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(payload: schemas.UserRegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter((models.User.username == payload.username) | (models.User.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    user = models.User(username=payload.username, email=payload.email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}


@app.post("/auth/login", response_model=schemas.TokenResponse)
def login(payload: schemas.UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.username)
    return schemas.TokenResponse(access_token=token)


@app.get("/transactions", response_model=list[schemas.TransactionResponse])
def get_transactions(
    tx_type: str | None = Query(default=None, alias="type"),
    category: str | None = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return transaction.list_transactions(db, current_user.id, tx_type, category)


@app.post("/transactions", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
def add_transaction(
    payload: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return transaction.create_transaction(db, current_user.id, payload)


@app.put("/transactions/{tx_id}", response_model=schemas.TransactionResponse)
def update_transaction(
    tx_id: int,
    payload: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    tx = transaction.update_transaction(db, current_user.id, tx_id, payload)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx


@app.delete("/transactions/{tx_id}")
def remove_transaction(tx_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    deleted = transaction.delete_transaction(db, current_user.id, tx_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted"}


@app.get("/transactions/search", response_model=list[schemas.TransactionResponse])
def search_transaction(
    q: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return transaction.search_transactions(db, current_user.id, q)


@app.get("/budgets", response_model=list[schemas.BudgetResponse])
def get_budgets(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return budget.list_budgets(db, current_user.id)


@app.post("/budgets", response_model=schemas.BudgetResponse, status_code=status.HTTP_201_CREATED)
def set_budget(
    payload: schemas.BudgetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return budget.upsert_budget(db, current_user.id, payload)


@app.get("/budgets/status", response_model=list[schemas.BudgetStatusItem])
def budget_overview(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return budget.budget_status(db, current_user.id)


def _all_user_transactions(db: Session, user_id: int):
    return transaction.list_transactions(db, user_id)


@app.get("/analytics/summary", response_model=schemas.SummaryResponse)
def analytics_summary(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return analytics.calculate_summary(_all_user_transactions(db, current_user.id))


@app.get("/analytics/by-category", response_model=list[schemas.CategoryBreakdownItem])
def analytics_by_category(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return analytics.spending_by_category(_all_user_transactions(db, current_user.id))


@app.get("/analytics/monthly-trend", response_model=list[schemas.MonthlyTrendItem])
def analytics_monthly_trend(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return analytics.monthly_trend(_all_user_transactions(db, current_user.id))


@app.get("/analytics/top-expenses", response_model=list[schemas.CategoryBreakdownItem])
def analytics_top_expenses(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return analytics.top_expense_categories(_all_user_transactions(db, current_user.id))


@app.post("/ai/advice", response_model=schemas.AdviceResponse)
def ai_finance_advice(
    _payload: schemas.AdviceRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    summary = analytics.calculate_summary(_all_user_transactions(db, current_user.id))
    return schemas.AdviceResponse(advice=get_advice(summary))


@app.post("/ai/question", response_model=schemas.AdviceResponse)
def ai_finance_question(
    payload: schemas.QuestionRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    summary = analytics.calculate_summary(_all_user_transactions(db, current_user.id))
    return schemas.AdviceResponse(advice=answer_question(summary, payload.question))


@app.get("/reports/weekly", response_model=schemas.ReportSummary)
def weekly_report(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    data = reports.filter_transactions_by_days(_all_user_transactions(db, current_user.id), 7)
    return reports.summarize_period(data, "weekly")


@app.get("/reports/monthly", response_model=schemas.ReportSummary)
def monthly_report(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    data = reports.filter_transactions_by_days(_all_user_transactions(db, current_user.id), 30)
    return reports.summarize_period(data, "monthly")


@app.get("/reports/export-csv")
def export_csv(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    data = _all_user_transactions(db, current_user.id)
    return reports.export_csv(data)
