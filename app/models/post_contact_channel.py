import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class PostContactChannel(Base):
    """Messenger channel for a post contact"""

    __tablename__ = "post_contact_channels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_contact_id = Column(UUID(as_uuid=True), ForeignKey("post_contacts.id"), nullable=False)
    type = Column(String(30), nullable=False)
    value = Column(String(255), nullable=False)
    label = Column(String(100), nullable=True)
    is_primary = Column(Boolean, default=False)

    post_contact = relationship("PostContact", back_populates="channels")

    def __repr__(self):
        return f"<PostContactChannel(id={self.id}, type={self.type})>"
