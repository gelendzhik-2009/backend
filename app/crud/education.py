from uuid import UUID
from sqlalchemy.orm import Session
from app.models.education import Education


def get_educations(db: Session, profile_id: UUID) -> list[Education]:
    """Get all education records for a profile"""
    return db.query(Education).filter(Education.applicant_profile_id == profile_id).all()


def create_education(db: Session, profile_id: UUID, data: dict) -> Education:
    """Create education record"""
    db_edu = Education(applicant_profile_id=profile_id, **data)
    db.add(db_edu)
    db.commit()
    db.refresh(db_edu)
    return db_edu


def update_education(db: Session, db_edu: Education, data: dict) -> Education:
    """Update education record"""
    for field, value in data.items():
        setattr(db_edu, field, value)
    db.commit()
    db.refresh(db_edu)
    return db_edu


def delete_education(db: Session, education_id: UUID) -> bool:
    """Delete education record"""
    db_edu = db.query(Education).filter(Education.id == education_id).first()
    if db_edu:
        db.delete(db_edu)
        db.commit()
        return True
    return False
