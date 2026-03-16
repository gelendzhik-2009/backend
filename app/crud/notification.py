from uuid import UUID
from sqlalchemy.orm import Session
from app.models.notification import Notification


def get_notifications(db: Session, user_id: UUID, unread_only: bool = False) -> list[Notification]:
    """Get notifications for a user"""
    query = db.query(Notification).filter(Notification.user_id == user_id)
    if unread_only:
        query = query.filter(Notification.is_read.is_(False))
    return query.order_by(Notification.created_at.desc()).all()


def create_notification(db: Session, user_id: UUID, notif_type: str, title: str, message: str = None, reference_id: UUID = None) -> Notification:
    """Create a notification"""
    db_notif = Notification(user_id=user_id, type=notif_type, title=title, message=message, reference_id=reference_id)
    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)
    return db_notif


def mark_notification_read(db: Session, notification_id: UUID) -> Notification:
    """Mark a single notification as read"""
    db_notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if db_notif:
        db_notif.is_read = True
        db.commit()
        db.refresh(db_notif)
    return db_notif


def mark_all_read(db: Session, user_id: UUID) -> int:
    """Mark all notifications as read, return count updated"""
    count = db.query(Notification).filter(
        Notification.user_id == user_id, Notification.is_read.is_(False)
    ).update({"is_read": True}, synchronize_session="fetch")
    db.commit()
    return count
