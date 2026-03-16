import uuid
from sqlalchemy import Column, String, Text, Date, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Project(Base):
    """Applicant portfolio project"""

    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    applicant_profile_id = Column(UUID(as_uuid=True), ForeignKey("applicant_profiles.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    role_name = Column(String(150), nullable=True)
    project_url = Column(Text, nullable=True)
    demo_url = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_ongoing = Column(Boolean, default=False)

    applicant_profile = relationship("ApplicantProfile", back_populates="projects")
    repositories = relationship("ProjectRepository", back_populates="project", cascade="all, delete-orphan")
    skills = relationship("Skill", secondary="project_skills", back_populates="projects")

    def __repr__(self):
        return f"<Project(id={self.id}, title={self.title})>"
