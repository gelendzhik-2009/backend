from uuid import UUID
from sqlalchemy.orm import Session
from app.models.application import Application


def get_application(db: Session, application_id: UUID) -> Application:
    """Get application by ID"""
    return db.query(Application).filter(Application.id == application_id).first()


def get_applications_by_post(db: Session, post_id: UUID) -> list[Application]:
    """Get all applications for a post"""
    return db.query(Application).filter(Application.post_id == post_id).all()


def get_applications_by_user(db: Session, user_id: UUID) -> list[Application]:
    """Get all applications by a user"""
    return db.query(Application).filter(Application.applicant_id == user_id).all()


def create_application(db: Session, post_id: UUID, applicant_id: UUID, cover_letter: str = None) -> Application:
    """Create a new application"""
    db_app = Application(post_id=post_id, applicant_id=applicant_id, cover_letter=cover_letter)
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app


def update_application_status(db: Session, db_app: Application, new_status: str) -> Application:
    """Update application status"""
    db_app.status = new_status
    db.commit()
    db.refresh(db_app)
    return db_app


def delete_application(db: Session, application_id: UUID) -> bool:
    """Delete/withdraw application"""
    db_app = db.query(Application).filter(Application.id == application_id).first()
    if db_app:
        db.delete(db_app)
        db.commit()
        return True
    return False
