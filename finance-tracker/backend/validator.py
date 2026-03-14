from datetime import date


def month_from_date(value: date) -> str:
    return value.strftime("%Y-%m")


def sanitize_search_query(value: str) -> str:
    return value.strip()[:100]
