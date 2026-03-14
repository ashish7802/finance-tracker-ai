import csv
from datetime import date, timedelta
from pathlib import Path

from fastapi.responses import FileResponse

import models
from analytics import calculate_summary
from schemas import ReportSummary


REPORTS_DIR = Path(__file__).resolve().parent / "generated_reports"
REPORTS_DIR.mkdir(exist_ok=True)


def summarize_period(transactions: list[models.Transaction], period: str) -> ReportSummary:
    summary = calculate_summary(transactions)
    return ReportSummary(period=period, income=summary.total_income, expense=summary.total_expense, net=summary.savings)


def filter_transactions_by_days(transactions: list[models.Transaction], days: int) -> list[models.Transaction]:
    cutoff = date.today() - timedelta(days=days)
    return [tx for tx in transactions if tx.date >= cutoff]


def export_csv(transactions: list[models.Transaction]) -> FileResponse:
    output_file = REPORTS_DIR / "transactions_export.csv"
    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "type", "amount", "category", "description", "date"])
        for tx in transactions:
            writer.writerow([tx.id, tx.type, tx.amount, tx.category, tx.description or "", tx.date.isoformat()])

    return FileResponse(path=output_file, media_type="text/csv", filename="transactions_export.csv")
