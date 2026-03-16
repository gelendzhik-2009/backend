from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database import Base


class Hashtag(Base):
    """Content hashtag for posts"""

    __tablename__ = "hashtags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)

    posts = relationship("Post", secondary="post_hashtags", back_populates="hashtags")

    def __repr__(self):
        return f"<Hashtag(id={self.id}, name={self.name})>"
