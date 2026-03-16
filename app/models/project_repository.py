import uuid
from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class ProjectRepository(Base):
    """Repository link for a project"""

    __tablename__ = "project_repositories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    url = Column(Text, nullable=False)
    label = Column(String(100), nullable=True)
    is_primary = Column(Boolean, default=False)

    project = relationship("Project", back_populates="repositories")

    def __repr__(self):
        return f"<ProjectRepository(id={self.id}, url={self.url})>"
