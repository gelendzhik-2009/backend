import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Post(Base):
    """Base post aggregator — each post_type has a detail table"""

    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    type = Column(String(30), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="ACTIVE", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    author = relationship("User", back_populates="posts")
    company = relationship("Company", back_populates="posts")
    contact = relationship("PostContact", back_populates="post", uselist=False, cascade="all, delete-orphan")
    vacancy = relationship("VacancyPost", back_populates="post", uselist=False, cascade="all, delete-orphan")
    internship = relationship("InternshipPost", back_populates="post", uselist=False, cascade="all, delete-orphan")
    event = relationship("EventPost", back_populates="post", uselist=False, cascade="all, delete-orphan")
    mentoring = relationship("MentoringPost", back_populates="post", uselist=False, cascade="all, delete-orphan")
    simple = relationship("SimplePost", back_populates="post", uselist=False, cascade="all, delete-orphan")
    skills = relationship("Skill", secondary="post_skills", back_populates="posts")
    hashtags = relationship("Hashtag", secondary="post_hashtags", back_populates="posts")
    applications = relationship("Application", back_populates="post")
    favorites = relationship("Favorite", back_populates="post")

    def __repr__(self):
        return f"<Post(id={self.id}, type={self.type}, status={self.status})>"
