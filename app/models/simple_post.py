import uuid
from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class SimplePost(Base):
    """Detail table for simple POST type — text only"""

    __tablename__ = "simple_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)

    post = relationship("Post", back_populates="simple")

    def __repr__(self):
        return f"<SimplePost(id={self.id})>"
