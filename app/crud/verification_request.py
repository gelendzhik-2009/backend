from uuid import UUID
from sqlalchemy.orm import Session
from app.models.verification_request import VerificationRequest
from app.models.company import Company
from datetime import datetime, timezone


def get_verification_request(db: Session, request_id: UUID) -> VerificationRequest:
    """Get verification request by ID"""
    return db.query(VerificationRequest).filter(VerificationRequest.id == request_id).first()


def get_requests_by_company(db: Session, company_id: UUID) -> list[VerificationRequest]:
    """Get all verification requests for a company"""
    return db.query(VerificationRequest).filter(VerificationRequest.company_id == company_id).all()


def get_pending_requests(db: Session, skip: int = 0, limit: int = 50) -> list[VerificationRequest]:
    """Get pending verification requests"""
    return db.query(VerificationRequest).filter(
        VerificationRequest.status == "PENDING"
    ).offset(skip).limit(limit).all()


def create_verification_request(db: Session, company_id: UUID, data: dict) -> VerificationRequest:
    """Submit a verification request"""
    db_req = VerificationRequest(company_id=company_id, **data)
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req


def review_verification(db: Session, db_req: VerificationRequest, reviewer_id: UUID, approved: bool, reason: str = None) -> VerificationRequest:
    """Approve or reject a verification request"""
    db_req.status = "APPROVED" if approved else "REJECTED"
    db_req.reviewed_by = reviewer_id
    db_req.reviewed_at = datetime.now(timezone.utc)
    db_req.rejection_reason = reason

    if approved:
        company = db.query(Company).filter(Company.id == db_req.company_id).first()
        if company:
            company.is_verified = True
            company.verified_at = datetime.now(timezone.utc)
            company.verified_by = reviewer_id

    db.commit()
    db.refresh(db_req)
    return db_req
