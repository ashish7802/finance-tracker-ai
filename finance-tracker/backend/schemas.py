from datetime import date
from pydantic import BaseModel, Field, field_validator


class UserRegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)
    email: str


    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("invalid email format")
        return value


class UserLoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TransactionBase(BaseModel):
    type: str
    amount: float = Field(gt=0)
    category: str = Field(min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    date: date

    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str) -> str:
        normalized = value.lower()
        if normalized not in {"income", "expense"}:
            raise ValueError("type must be 'income' or 'expense'")
        return normalized


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    type: str | None = None
    amount: float | None = Field(default=None, gt=0)
    category: str | None = Field(default=None, min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    date: date | None = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, value: str | None) -> str | None:
        if value is None:
            return value
        normalized = value.lower()
        if normalized not in {"income", "expense"}:
            raise ValueError("type must be 'income' or 'expense'")
        return normalized


class TransactionResponse(TransactionBase):
    id: int

    class Config:
        from_attributes = True


class BudgetCreate(BaseModel):
    category: str = Field(min_length=2, max_length=50)
    amount: float = Field(gt=0)
    month: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")


class BudgetResponse(BudgetCreate):
    id: int

    class Config:
        from_attributes = True


class BudgetStatusItem(BaseModel):
    category: str
    month: str
    budget_amount: float
    actual_spending: float
    remaining: float
    percent_used: float


class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    savings: float
    savings_rate: float


class CategoryBreakdownItem(BaseModel):
    category: str
    amount: float


class MonthlyTrendItem(BaseModel):
    month: str
    income: float
    expense: float


class AdviceRequest(BaseModel):
    month: str | None = None


class QuestionRequest(BaseModel):
    question: str = Field(min_length=5, max_length=500)


class AdviceResponse(BaseModel):
    advice: str


class ReportSummary(BaseModel):
    period: str
    income: float
    expense: float
    net: float
