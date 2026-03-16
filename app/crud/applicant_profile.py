from uuid import UUID
from sqlalchemy.orm import Session
from app.models.applicant_profile import ApplicantProfile


def get_profile_by_user(db: Session, user_id: UUID) -> ApplicantProfile:
    """Get applicant profile by user ID"""
    return db.query(ApplicantProfile).filter(ApplicantProfile.user_id == user_id).first()


def get_profile(db: Session, profile_id: UUID) -> ApplicantProfile:
    """Get applicant profile by its own ID"""
    return db.query(ApplicantProfile).filter(ApplicantProfile.id == profile_id).first()


def create_profile(db: Session, user_id: UUID, data: dict) -> ApplicantProfile:
    """Create applicant profile"""
    db_profile = ApplicantProfile(user_id=user_id, **data)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(db: Session, db_profile: ApplicantProfile, data: dict) -> ApplicantProfile:
    """Update applicant profile"""
    for field, value in data.items():
        setattr(db_profile, field, value)
    db.commit()
    db.refresh(db_profile)
    return db_profile
