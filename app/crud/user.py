from datetime import timedelta
from uuid import UUID
from sqlalchemy.orm import Session
from app.config import settings
from app.models.user import User
from app.security import create_access_token, get_password_hash, verify_password


def get_user(db: Session, user_id: UUID) -> User:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Get all users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, email: str, display_name: str, password: str, role: str) -> User:
    """Create a new user"""
    db_user = User(
        email=email,
        display_name=display_name,
        password_hash=get_password_hash(password),
        role=role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: User, update_data: dict) -> User:
    """Update user fields from dict"""
    if "password" in update_data and update_data["password"]:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    else:
        update_data.pop("password", None)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: UUID) -> bool:
    """Delete user by ID"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def authenticate_user(db: Session, email: str, password: str) -> User:
    """Authenticate user by email and password"""
    db_user = get_user_by_email(db, email)
    if not db_user or not verify_password(password, db_user.password_hash):
        return None
    return db_user


def generate_user_token(user: User) -> str:
    """Generate JWT access token for a user"""
    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={"sub": str(user.id)}, expires_delta=expires)