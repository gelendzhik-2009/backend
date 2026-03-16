import uuid
from sqlalchemy import Column, String, SmallInteger, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Education(Base):
    """Applicant education record"""

    __tablename__ = "educations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    applicant_profile_id = Column(UUID(as_uuid=True), ForeignKey("applicant_profiles.id"), nullable=False)
    organization_name = Column(String(255), nullable=False)
    degree = Column(String(150), nullable=True)
    field_of_study = Column(String(150), nullable=True)
    start_year = Column(SmallInteger, nullable=True)
    graduation_year = Column(SmallInteger, nullable=True)
    is_current = Column(Boolean, default=False)

    applicant_profile = relationship("ApplicantProfile", back_populates="educations")

    def __repr__(self):
        return f"<Education(id={self.id}, org={self.organization_name})>"
