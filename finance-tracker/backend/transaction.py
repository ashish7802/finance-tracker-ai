from sqlalchemy import or_
from sqlalchemy.orm import Session

import models
import schemas
from validator import sanitize_search_query


def list_transactions(db: Session, user_id: int, tx_type: str | None = None, category: str | None = None):
    query = db.query(models.Transaction).filter(models.Transaction.user_id == user_id)
    if tx_type:
        query = query.filter(models.Transaction.type == tx_type.lower())
    if category:
        query = query.filter(models.Transaction.category == category)
    return query.order_by(models.Transaction.date.desc()).all()


def create_transaction(db: Session, user_id: int, payload: schemas.TransactionCreate):
    tx = models.Transaction(user_id=user_id, **payload.model_dump())
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def update_transaction(db: Session, user_id: int, tx_id: int, payload: schemas.TransactionUpdate):
    tx = db.query(models.Transaction).filter(models.Transaction.id == tx_id, models.Transaction.user_id == user_id).first()
    if not tx:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(tx, key, value)
    db.commit()
    db.refresh(tx)
    return tx


def delete_transaction(db: Session, user_id: int, tx_id: int) -> bool:
    tx = db.query(models.Transaction).filter(models.Transaction.id == tx_id, models.Transaction.user_id == user_id).first()
    if not tx:
        return False
    db.delete(tx)
    db.commit()
    return True


def search_transactions(db: Session, user_id: int, query_text: str):
    safe_query = sanitize_search_query(query_text)
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.user_id == user_id)
        .filter(
            or_(
                models.Transaction.description.ilike(f"%{safe_query}%"),
                models.Transaction.category.ilike(f"%{safe_query}%"),
            )
        )
        .order_by(models.Transaction.date.desc())
        .all()
    )
