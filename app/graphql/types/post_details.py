"""GraphQL types for post detail tables: Vacancy, Internship, Event, Mentoring, Simple"""

import uuid as _uuid
from datetime import datetime
from typing import Optional
import strawberry
from sqlalchemy.orm import Session
from app.graphql.types.company import AddressType


@strawberry.type
class VacancyPostType:
    id: _uuid.UUID
    title: str
    description: str
    work_format: str
    employment_type: str
    experience_level: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency_code: Optional[str] = None
    salary_period: Optional[str] = None
    is_gross: Optional[bool] = False
    expires_at: datetime = strawberry.UNSET
    address: Optional[AddressType] = None


@strawberry.type
class InternshipPostType:
    id: _uuid.UUID
    title: str
    description: str
    work_format: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency_code: Optional[str] = None
    salary_period: Optional[str] = None
    is_gross: Optional[bool] = False
    duration_months: Optional[int] = None
    starts_at: datetime = strawberry.UNSET
    expires_at: datetime = strawberry.UNSET
    address: Optional[AddressType] = None


@strawberry.type
class EventPostType:
    id: _uuid.UUID
    title: str
    description: str
    event_date: datetime = strawberry.UNSET
    event_end_date: Optional[datetime] = None
    is_online: bool = False
    external_url: Optional[str] = None
    address: Optional[AddressType] = None


@strawberry.type
class MentoringPostType:
    id: _uuid.UUID
    title: str
    description: str
    is_online: bool = False
    capacity: Optional[int] = None
    duration_months: Optional[int] = None
    starts_at: datetime = strawberry.UNSET
    expires_at: datetime = strawberry.UNSET
    address: Optional[AddressType] = None


@strawberry.type
class SimplePostType:
    id: _uuid.UUID
    description: str
    image_url: Optional[str] = None


def _addr(db_addr) -> Optional[AddressType]:
    if not db_addr:
        return None
    return AddressType(
        id=db_addr.id, country_code=db_addr.country_code, region=db_addr.region,
        city=db_addr.city, postal_code=db_addr.postal_code, address_line=db_addr.address_line,
        latitude=float(db_addr.latitude), longitude=float(db_addr.longitude),
    )


def load_vacancy(db: Session, post_id: _uuid.UUID) -> Optional[VacancyPostType]:
    from app.models.vacancy_post import VacancyPost
    row = db.query(VacancyPost).filter(VacancyPost.post_id == post_id).first()
    if not row:
        return None
    return VacancyPostType(
        id=row.id, title=row.title, description=row.description,
        work_format=row.work_format, employment_type=row.employment_type,
        experience_level=row.experience_level, salary_min=float(row.salary_min) if row.salary_min else None,
        salary_max=float(row.salary_max) if row.salary_max else None, currency_code=row.currency_code,
        salary_period=row.salary_period, is_gross=row.is_gross, expires_at=row.expires_at,
        address=_addr(row.address),
    )


def load_internship(db: Session, post_id: _uuid.UUID) -> Optional[InternshipPostType]:
    from app.models.internship_post import InternshipPost
    row = db.query(InternshipPost).filter(InternshipPost.post_id == post_id).first()
    if not row:
        return None
    return InternshipPostType(
        id=row.id, title=row.title, description=row.description, work_format=row.work_format,
        salary_min=float(row.salary_min) if row.salary_min else None,
        salary_max=float(row.salary_max) if row.salary_max else None,
        currency_code=row.currency_code, salary_period=row.salary_period,
        is_gross=row.is_gross, duration_months=row.duration_months,
        starts_at=row.starts_at, expires_at=row.expires_at, address=_addr(row.address),
    )


def load_event(db: Session, post_id: _uuid.UUID) -> Optional[EventPostType]:
    from app.models.event_post import EventPost
    row = db.query(EventPost).filter(EventPost.post_id == post_id).first()
    if not row:
        return None
    return EventPostType(
        id=row.id, title=row.title, description=row.description,
        event_date=row.event_date, event_end_date=row.event_end_date,
        is_online=row.is_online, external_url=row.external_url, address=_addr(row.address),
    )


def load_mentoring(db: Session, post_id: _uuid.UUID) -> Optional[MentoringPostType]:
    from app.models.mentoring_post import MentoringPost
    row = db.query(MentoringPost).filter(MentoringPost.post_id == post_id).first()
    if not row:
        return None
    return MentoringPostType(
        id=row.id, title=row.title, description=row.description,
        is_online=row.is_online, capacity=row.capacity,
        duration_months=row.duration_months, starts_at=row.starts_at,
        expires_at=row.expires_at, address=_addr(row.address),
    )


def load_simple(db: Session, post_id: _uuid.UUID) -> Optional[SimplePostType]:
    from app.models.simple_post import SimplePost
    row = db.query(SimplePost).filter(SimplePost.post_id == post_id).first()
    if not row:
        return None
    return SimplePostType(id=row.id, description=row.description, image_url=row.image_url)
