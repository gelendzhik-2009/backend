import uuid
from sqlalchemy import Column, String, Text, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class VacancyPost(Base):
    """Detail table for VACANCY post type"""

    __tablename__ = "vacancy_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), unique=True, nullable=False)
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    work_format = Column(String(20), nullable=False)
    employment_type = Column(String(20), nullable=False)
    experience_level = Column(String(20), nullable=False)
    salary_min = Column(Numeric(12, 2), nullable=True)
    salary_max = Column(Numeric(12, 2), nullable=True)
    currency_code = Column(String(3), nullable=True)
    salary_period = Column(String(20), nullable=True)
    is_gross = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    post = relationship("Post", back_populates="vacancy")
    address = relationship("Address", back_populates="vacancy_posts")

    def __repr__(self):
        return f"<VacancyPost(id={self.id}, title={self.title})>"
