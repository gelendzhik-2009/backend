import uuid
from sqlalchemy import Column, String, Text, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Address(Base):
    """Reusable address record with geolocation"""

    __tablename__ = "addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_code = Column(String(2), nullable=False)
    region = Column(String(150), nullable=True)
    city = Column(String(150), nullable=False)
    postal_code = Column(String(32), nullable=True)
    address_line = Column(Text, nullable=False)
    latitude = Column(Numeric(9, 6), nullable=False)
    longitude = Column(Numeric(9, 6), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    companies = relationship("Company", back_populates="address")
    vacancy_posts = relationship("VacancyPost", back_populates="address")
    internship_posts = relationship("InternshipPost", back_populates="address")
    event_posts = relationship("EventPost", back_populates="address")
    mentoring_posts = relationship("MentoringPost", back_populates="address")

    def __repr__(self):
        return f"<Address(id={self.id}, city={self.city})>"
