import uuid
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class EventPost(Base):
    """Detail table for EVENT post type"""

    __tablename__ = "event_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), unique=True, nullable=False)
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    event_date = Column(DateTime(timezone=True), nullable=False)
    event_end_date = Column(DateTime(timezone=True), nullable=True)
    is_online = Column(Boolean, nullable=False, default=False)
    external_url = Column(Text, nullable=True)

    post = relationship("Post", back_populates="event")
    address = relationship("Address", back_populates="event_posts")

    def __repr__(self):
        return f"<EventPost(id={self.id}, title={self.title})>"
