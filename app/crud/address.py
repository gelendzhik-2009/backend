from uuid import UUID
from sqlalchemy.orm import Session
from app.models.address import Address


def get_address(db: Session, address_id: UUID) -> Address:
    """Get address by ID"""
    return db.query(Address).filter(Address.id == address_id).first()


def create_address(db: Session, data: dict) -> Address:
    """Create a new address"""
    db_addr = Address(**data)
    db.add(db_addr)
    db.commit()
    db.refresh(db_addr)
    return db_addr


def update_address(db: Session, db_addr: Address, data: dict) -> Address:
    """Update address"""
    for field, value in data.items():
        setattr(db_addr, field, value)
    db.commit()
    db.refresh(db_addr)
    return db_addr
