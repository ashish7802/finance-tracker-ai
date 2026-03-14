from datetime import datetime, timedelta


def utc_now() -> datetime:
    return datetime.utcnow()


def period_bounds(days: int) -> tuple[datetime, datetime]:
    end = utc_now()
    start = end - timedelta(days=days)
    return start, end
