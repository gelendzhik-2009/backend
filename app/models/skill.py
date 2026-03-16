from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database import Base


class Skill(Base):
    """Technology or skill tag"""

    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False, index=True)

    posts = relationship("Post", secondary="post_skills", back_populates="skills")
    applicants = relationship("ApplicantProfile", secondary="applicant_skills", back_populates="skills")
    projects = relationship("Project", secondary="project_skills", back_populates="skills")

    def __repr__(self):
        return f"<Skill(id={self.id}, name={self.name})>"
