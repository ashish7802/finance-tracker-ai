from sqlalchemy import and_, func
from sqlalchemy.orm import Session

import models
import schemas


def list_budgets(db: Session, user_id: int):
    return db.query(models.Budget).filter(models.Budget.user_id == user_id).order_by(models.Budget.month.desc()).all()


def upsert_budget(db: Session, user_id: int, payload: schemas.BudgetCreate):
    budget = (
        db.query(models.Budget)
        .filter(models.Budget.user_id == user_id, models.Budget.category == payload.category, models.Budget.month == payload.month)
        .first()
    )
    if budget:
        budget.amount = payload.amount
    else:
        budget = models.Budget(user_id=user_id, **payload.model_dump())
        db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def budget_status(db: Session, user_id: int):
    budgets = list_budgets(db, user_id)
    response: list[schemas.BudgetStatusItem] = []
    for item in budgets:
        spent = (
            db.query(func.coalesce(func.sum(models.Transaction.amount), 0.0))
            .filter(
                and_(
                    models.Transaction.user_id == user_id,
                    models.Transaction.type == "expense",
                    models.Transaction.category == item.category,
                    func.strftime("%Y-%m", models.Transaction.date) == item.month,
                )
            )
            .scalar()
        )
        remaining = item.amount - spent
        percent_used = (spent / item.amount * 100) if item.amount else 0
        response.append(
            schemas.BudgetStatusItem(
                category=item.category,
                month=item.month,
                budget_amount=round(item.amount, 2),
                actual_spending=round(spent, 2),
                remaining=round(remaining, 2),
                percent_used=round(percent_used, 2),
            )
        )
    return response
