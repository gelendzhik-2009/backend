import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class PostContact(Base):
    """Contact information block for a post"""

    __tablename__ = "post_contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), unique=True, nullable=False)
    contact_person = Column(String(150), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    website_url = Column(Text, nullable=True)
    apply_url = Column(Text, nullable=True)
    note = Column(Text, nullable=True)

    post = relationship("Post", back_populates="contact")
    channels = relationship("PostContactChannel", back_populates="post_contact", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PostContact(id={self.id}, post_id={self.post_id})>"
