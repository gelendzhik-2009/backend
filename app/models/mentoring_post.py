import uuid
from sqlalchemy import Column, String, Text, Boolean, Integer, SmallInteger, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class MentoringPost(Base):
    """Detail table for MENTORING_PROGRAM post type"""

    __tablename__ = "mentoring_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), unique=True, nullable=False)
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    is_online = Column(Boolean, nullable=False, default=False)
    capacity = Column(Integer, nullable=True)
    duration_months = Column(SmallInteger, nullable=True)
    starts_at = Column(DateTime(timezone=True), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    post = relationship("Post", back_populates="mentoring")
    address = relationship("Address", back_populates="mentoring_posts")

    def __repr__(self):
        return f"<MentoringPost(id={self.id}, title={self.title})>"
