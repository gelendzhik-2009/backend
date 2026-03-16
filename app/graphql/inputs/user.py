"""Input types for user and applicant profile mutations"""

import uuid as _uuid
from datetime import date
from typing import Optional
import strawberry


@strawberry.input
class UpdateUserInput:
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    password: Optional[str] = None


@strawberry.input
class UpdateApplicantProfileInput:
    given_name: Optional[str] = None
    middle_name: Optional[str] = None
    family_name: Optional[str] = None
    bio: Optional[str] = None
    resume_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    profile_visibility: Optional[str] = None
    hide_applications: Optional[bool] = None


@strawberry.input
class EducationInput:
    organization_name: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_year: Optional[int] = None
    graduation_year: Optional[int] = None
    is_current: Optional[bool] = False


@strawberry.input
class ProjectInput:
    title: str
    description: str
    role_name: Optional[str] = None
    project_url: Optional[str] = None
    demo_url: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_ongoing: Optional[bool] = False


@strawberry.input
class ProjectRepositoryInput:
    url: str
    label: Optional[str] = None
    is_primary: Optional[bool] = False
