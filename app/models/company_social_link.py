import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class CompanySocialLink(Base):
    """Social media link for a company"""

    __tablename__ = "company_social_links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    platform_name = Column(String(100), nullable=False)
    url = Column(Text, nullable=False)

    company = relationship("Company", back_populates="social_links")

    def __repr__(self):
        return f"<CompanySocialLink(id={self.id}, platform={self.platform_name})>"
