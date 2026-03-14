import anthropic

from config import get_settings
from schemas import SummaryResponse


def _build_prompt(summary: SummaryResponse, question: str | None = None) -> str:
    base = (
        "You are a personal finance advisor. Provide practical and concise advice in bullet points. "
        f"User summary: income={summary.total_income}, expense={summary.total_expense}, "
        f"savings={summary.savings}, savings_rate={summary.savings_rate}%."
    )
    if question:
        base += f" User question: {question}"
    else:
        base += " Suggest improvements for budgeting, spending cuts, and savings growth."
    return base


def get_advice(summary: SummaryResponse) -> str:
    return _call_anthropic(_build_prompt(summary))


def answer_question(summary: SummaryResponse, question: str) -> str:
    return _call_anthropic(_build_prompt(summary, question))


def _call_anthropic(prompt: str) -> str:
    settings = get_settings()
    if not settings.anthropic_api_key:
        return "ANTHROPIC_API_KEY is not configured. Add it in your .env file to enable AI advice."

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in response.content if hasattr(block, "text"))
