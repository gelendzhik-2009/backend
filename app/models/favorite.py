import uuid
from sqlalchemy import Column, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Favorite(Base):
    """User bookmark — either a post or a company"""

    __tablename__ = "favorites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "post_id IS NOT NULL OR company_id IS NOT NULL",
            name="ck_favorite_target",
        ),
    )

    user = relationship("User", back_populates="favorites")
    post = relationship("Post", back_populates="favorites")
    company = relationship("Company")

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id})>"
