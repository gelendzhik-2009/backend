import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Application(Base):
    """Applicant's application/response to a post"""

    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False)
    applicant_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(String(20), nullable=False, default="PENDING")
    cover_letter = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint("post_id", "applicant_id", name="uq_application_post_applicant"),
    )

    post = relationship("Post", back_populates="applications")
    applicant = relationship("User", back_populates="applications")

    def __repr__(self):
        return f"<Application(id={self.id}, status={self.status})>"
