from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session
from app.models.favorite import Favorite


def get_favorites_by_user(db: Session, user_id: UUID) -> list[Favorite]:
    """Get all favorites for a user"""
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()


def add_favorite(db: Session, user_id: UUID, post_id: Optional[UUID] = None, company_id: Optional[UUID] = None) -> Favorite:
    """Add a post or company to favorites"""
    db_fav = Favorite(user_id=user_id, post_id=post_id, company_id=company_id)
    db.add(db_fav)
    db.commit()
    db.refresh(db_fav)
    return db_fav


def remove_favorite(db: Session, favorite_id: UUID) -> bool:
    """Remove a favorite"""
    db_fav = db.query(Favorite).filter(Favorite.id == favorite_id).first()
    if db_fav:
        db.delete(db_fav)
        db.commit()
        return True
    return False
