from uuid import UUID
from sqlalchemy.orm import Session
from app.models.contact import Contact


def get_contacts_for_user(db: Session, user_id: UUID, status: str = None) -> list[Contact]:
    """Get contacts where user is requester or addressee"""
    query = db.query(Contact).filter(
        (Contact.requester_id == user_id) | (Contact.addressee_id == user_id)
    )
    if status:
        query = query.filter(Contact.status == status)
    return query.all()


def get_contact(db: Session, contact_id: UUID) -> Contact:
    """Get contact by ID"""
    return db.query(Contact).filter(Contact.id == contact_id).first()


def create_contact_request(db: Session, requester_id: UUID, addressee_id: UUID) -> Contact:
    """Send a contact request"""
    db_contact = Contact(requester_id=requester_id, addressee_id=addressee_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def respond_to_contact(db: Session, db_contact: Contact, new_status: str) -> Contact:
    """Accept or reject a contact request"""
    db_contact.status = new_status
    db.commit()
    db.refresh(db_contact)
    return db_contact
