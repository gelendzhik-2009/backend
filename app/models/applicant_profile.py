import uuid
from sqlalchemy import Column, String, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class ApplicantProfile(Base):
    """Extended profile for applicant (EMPLOYEE) users"""

    __tablename__ = "applicant_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    given_name = Column(String(100), nullable=True)
    middle_name = Column(String(100), nullable=True)
    family_name = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    resume_url = Column(Text, nullable=True)
    portfolio_url = Column(Text, nullable=True)
    profile_visibility = Column(String(20), nullable=False, default="PRIVATE")
    hide_applications = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="applicant_profile")
    educations = relationship("Education", back_populates="applicant_profile", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="applicant_profile", cascade="all, delete-orphan")
    skills = relationship("Skill", secondary="applicant_skills", back_populates="applicants")

    def __repr__(self):
        return f"<ApplicantProfile(id={self.id}, user_id={self.user_id})>"
