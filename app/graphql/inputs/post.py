"""Input types for post mutations"""

import uuid as _uuid
from datetime import datetime
from typing import Optional
import strawberry
from app.graphql.inputs.company import AddressInput


@strawberry.input
class PostContactChannelInput:
    type: str
    value: str
    label: Optional[str] = None
    is_primary: Optional[bool] = False


@strawberry.input
class PostContactInput:
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website_url: Optional[str] = None
    apply_url: Optional[str] = None
    note: Optional[str] = None
    channels: Optional[list[PostContactChannelInput]] = None


@strawberry.input
class VacancyInput:
    title: str
    description: str
    work_format: str
    employment_type: str
    experience_level: str
    expires_at: datetime
    address: AddressInput
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency_code: Optional[str] = None
    salary_period: Optional[str] = None
    is_gross: Optional[bool] = False


@strawberry.input
class InternshipInput:
    title: str
    description: str
    work_format: str
    starts_at: datetime
    expires_at: datetime
    address: AddressInput
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency_code: Optional[str] = None
    salary_period: Optional[str] = None
    is_gross: Optional[bool] = False
    duration_months: Optional[int] = None


@strawberry.input
class EventInput:
    title: str
    description: str
    event_date: datetime
    is_online: bool = False
    event_end_date: Optional[datetime] = None
    external_url: Optional[str] = None
    address: Optional[AddressInput] = None


@strawberry.input
class MentoringInput:
    title: str
    description: str
    starts_at: datetime
    expires_at: datetime
    is_online: bool = False
    capacity: Optional[int] = None
    duration_months: Optional[int] = None
    address: Optional[AddressInput] = None


@strawberry.input
class SimplePostInput:
    description: str
    image_url: Optional[str] = None


@strawberry.input
class CreatePostInput:
    company_id: _uuid.UUID
    post_type: str
    contact: Optional[PostContactInput] = None
    skill_ids: Optional[list[int]] = None
    hashtag_ids: Optional[list[int]] = None
    vacancy: Optional[VacancyInput] = None
    internship: Optional[InternshipInput] = None
    event: Optional[EventInput] = None
    mentoring: Optional[MentoringInput] = None
    simple: Optional[SimplePostInput] = None
