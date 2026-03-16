from sqlalchemy.orm import Session
from app.models.hashtag import Hashtag


def get_hashtag(db: Session, hashtag_id: int) -> Hashtag:
    """Get hashtag by ID"""
    return db.query(Hashtag).filter(Hashtag.id == hashtag_id).first()


def get_hashtag_by_name(db: Session, name: str) -> Hashtag:
    """Get hashtag by name"""
    return db.query(Hashtag).filter(Hashtag.name == name).first()


def get_hashtags(db: Session, skip: int = 0, limit: int = 200) -> list[Hashtag]:
    """Get all hashtags"""
    return db.query(Hashtag).order_by(Hashtag.name).offset(skip).limit(limit).all()


def create_hashtag(db: Session, name: str) -> Hashtag:
    """Create a new hashtag"""
    db_tag = Hashtag(name=name)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag
