import uuid
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Company(Base):
    """Employer company profile"""

    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    industry = Column(String(150), nullable=True)
    website_url = Column(Text, nullable=True)
    logo_url = Column(Text, nullable=True)
    is_verified = Column(Boolean, nullable=False, default=False)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    owner = relationship("User", back_populates="companies", foreign_keys=[owner_id])
    verifier = relationship("User", foreign_keys=[verified_by])
    address = relationship("Address", back_populates="companies")
    social_links = relationship("CompanySocialLink", back_populates="company", cascade="all, delete-orphan")
    photos = relationship("CompanyPhoto", back_populates="company", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="company")
    verification_requests = relationship("VerificationRequest", back_populates="company")

    def __repr__(self):
        return f"<Company(id={self.id}, name={self.name})>"
