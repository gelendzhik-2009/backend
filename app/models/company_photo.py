import uuid
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class CompanyPhoto(Base):
    """Photo/image for a company gallery"""

    __tablename__ = "company_photos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    url = Column(Text, nullable=False)
    sort_order = Column(Integer, nullable=True)

    company = relationship("Company", back_populates="photos")

    def __repr__(self):
        return f"<CompanyPhoto(id={self.id}, company_id={self.company_id})>"
