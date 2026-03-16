import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """Platform user account"""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, index=True)
    avatar_url = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    applicant_profile = relationship("ApplicantProfile", back_populates="user", uselist=False)
    companies = relationship("Company", back_populates="owner", foreign_keys="Company.owner_id")
    posts = relationship("Post", back_populates="author")
    applications = relationship("Application", back_populates="applicant")
    favorites = relationship("Favorite", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
