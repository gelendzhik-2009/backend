from uuid import UUID
from sqlalchemy.orm import Session
from app.models.company import Company


def get_company(db: Session, company_id: UUID) -> Company:
    """Get company by ID"""
    return db.query(Company).filter(Company.id == company_id).first()


def get_companies_by_owner(db: Session, owner_id: UUID) -> list[Company]:
    """Get all companies owned by user"""
    return db.query(Company).filter(Company.owner_id == owner_id).all()


def get_companies(db: Session, skip: int = 0, limit: int = 100) -> list[Company]:
    """Get companies with pagination"""
    return db.query(Company).offset(skip).limit(limit).all()


def create_company(db: Session, owner_id: UUID, data: dict) -> Company:
    """Create a new company"""
    db_company = Company(owner_id=owner_id, **data)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def update_company(db: Session, db_company: Company, data: dict) -> Company:
    """Update company fields"""
    for field, value in data.items():
        setattr(db_company, field, value)
    db.commit()
    db.refresh(db_company)
    return db_company


def delete_company(db: Session, company_id: UUID) -> bool:
    """Delete company"""
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if db_company:
        db.delete(db_company)
        db.commit()
        return True
    return False
