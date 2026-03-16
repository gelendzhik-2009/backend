from uuid import UUID
from sqlalchemy.orm import Session
from app.models.recommendation import Recommendation


def get_recommendations_for_user(db: Session, receiver_id: UUID) -> list[Recommendation]:
    """Get recommendations received by a user"""
    return db.query(Recommendation).filter(Recommendation.receiver_id == receiver_id).all()


def create_recommendation(db: Session, sender_id: UUID, receiver_id: UUID, post_id: UUID, message: str = None) -> Recommendation:
    """Create a recommendation"""
    db_rec = Recommendation(sender_id=sender_id, receiver_id=receiver_id, post_id=post_id, message=message)
    db.add(db_rec)
    db.commit()
    db.refresh(db_rec)
    return db_rec
