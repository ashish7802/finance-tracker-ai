from collections import defaultdict

import models
import schemas


def calculate_summary(transactions: list[models.Transaction]) -> schemas.SummaryResponse:
    income = sum(t.amount for t in transactions if t.type == "income")
    expense = sum(t.amount for t in transactions if t.type == "expense")
    savings = income - expense
    savings_rate = (savings / income * 100) if income > 0 else 0.0
    return schemas.SummaryResponse(
        total_income=round(income, 2),
        total_expense=round(expense, 2),
        savings=round(savings, 2),
        savings_rate=round(savings_rate, 2),
    )


def spending_by_category(transactions: list[models.Transaction]) -> list[schemas.CategoryBreakdownItem]:
    totals: dict[str, float] = defaultdict(float)
    for tx in transactions:
        if tx.type == "expense":
            totals[tx.category] += tx.amount
    return [schemas.CategoryBreakdownItem(category=k, amount=round(v, 2)) for k, v in sorted(totals.items(), key=lambda x: x[1], reverse=True)]


def monthly_trend(transactions: list[models.Transaction]) -> list[schemas.MonthlyTrendItem]:
    aggregate: dict[str, dict[str, float]] = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for tx in transactions:
        month = tx.date.strftime("%Y-%m")
        aggregate[month][tx.type] += tx.amount
    result = [
        schemas.MonthlyTrendItem(month=month, income=round(vals["income"], 2), expense=round(vals["expense"], 2))
        for month, vals in sorted(aggregate.items())
    ]
    return result


def top_expense_categories(transactions: list[models.Transaction], limit: int = 5) -> list[schemas.CategoryBreakdownItem]:
    by_category = spending_by_category(transactions)
    return by_category[:limit]
