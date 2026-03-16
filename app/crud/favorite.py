from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session
from app.models.favorite import Favorite


def get_favorites_by_user(db: Session, user_id: UUID) -> list[Favorite]:
    """Get all favorites for a user"""
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()


def toggle_favorite(db: Session, user_id: UUID, post_id: Optional[UUID] = None, company_id: Optional[UUID] = None):
    """Toggle a favorite: remove if exists, create if not. Returns (Favorite|None, created:bool)"""
    if bool(post_id) == bool(company_id):
        raise ValueError("Exactly one of post_id or company_id must be provided")
    query = db.query(Favorite).filter(Favorite.user_id == user_id)
    if post_id:
        query = query.filter(Favorite.post_id == post_id)
    else:
        query = query.filter(Favorite.company_id == company_id)
    existing = query.first()
    if existing:
        db.delete(existing)
        db.commit()
        return existing, False
    db_fav = Favorite(user_id=user_id, post_id=post_id, company_id=company_id)
    db.add(db_fav)
    db.commit()
    db.refresh(db_fav)
    return db_fav, True


def remove_favorite(db: Session, user_id: UUID, favorite_id: UUID) -> bool:
    """Remove a favorite belonging to a specific user"""
    db_fav = db.query(Favorite).filter(Favorite.id == favorite_id, Favorite.user_id == user_id).first()
    if db_fav:
        db.delete(db_fav)
        db.commit()
        return True
    return False
