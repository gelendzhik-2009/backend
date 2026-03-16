"""GraphQL types for User, ApplicantProfile, Education, Project"""

import uuid as _uuid
from datetime import datetime, date
from typing import Optional
import strawberry
from strawberry.types import Info


@strawberry.type
class EducationType:
    id: _uuid.UUID
    organization_name: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_year: Optional[int] = None
    graduation_year: Optional[int] = None
    is_current: Optional[bool] = False


@strawberry.type
class ProjectRepositoryType:
    id: _uuid.UUID
    url: str
    label: Optional[str] = None
    is_primary: Optional[bool] = False


@strawberry.type
class SkillType:
    id: int
    name: str


@strawberry.type
class ProjectType:
    id: _uuid.UUID
    title: str
    description: str
    role_name: Optional[str] = None
    project_url: Optional[str] = None
    demo_url: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_ongoing: Optional[bool] = False

    @strawberry.field
    def repositories(self, info: Info) -> list[ProjectRepositoryType]:
        from app.models.project_repository import ProjectRepository
        db = info.context.db
        rows = db.query(ProjectRepository).filter(ProjectRepository.project_id == self.id).all()
        return [ProjectRepositoryType(id=r.id, url=r.url, label=r.label, is_primary=r.is_primary) for r in rows]

    @strawberry.field
    def skills(self, info: Info) -> list[SkillType]:
        from app.models.project import Project
        db_proj = info.context.db.query(Project).filter(Project.id == self.id).first()
        return [SkillType(id=s.id, name=s.name) for s in db_proj.skills] if db_proj else []


@strawberry.type
class ApplicantProfileType:
    id: _uuid.UUID
    user_id: _uuid.UUID
    given_name: Optional[str] = None
    middle_name: Optional[str] = None
    family_name: Optional[str] = None
    bio: Optional[str] = None
    resume_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    profile_visibility: str = "PRIVATE"
    hide_applications: bool = False

    @strawberry.field
    def educations(self, info: Info) -> list[EducationType]:
        from app.crud.education import get_educations
        rows = get_educations(info.context.db, self.id)
        return [EducationType(
            id=e.id, organization_name=e.organization_name, degree=e.degree,
            field_of_study=e.field_of_study, start_year=e.start_year,
            graduation_year=e.graduation_year, is_current=e.is_current,
        ) for e in rows]

    @strawberry.field
    def projects(self, info: Info) -> list[ProjectType]:
        from app.crud.project import get_projects
        rows = get_projects(info.context.db, self.id)
        return [ProjectType(
            id=p.id, title=p.title, description=p.description, role_name=p.role_name,
            project_url=p.project_url, demo_url=p.demo_url, start_date=p.start_date,
            end_date=p.end_date, is_ongoing=p.is_ongoing,
        ) for p in rows]

    @strawberry.field
    def skills(self, info: Info) -> list[SkillType]:
        from app.models.applicant_profile import ApplicantProfile
        db_profile = info.context.db.query(ApplicantProfile).filter(ApplicantProfile.id == self.id).first()
        return [SkillType(id=s.id, name=s.name) for s in db_profile.skills] if db_profile else []


@strawberry.type
class UserType:
    id: _uuid.UUID
    email: str
    display_name: str
    role: str
    avatar_url: Optional[str] = None
    is_active: bool = True
    created_at: datetime = strawberry.UNSET
    updated_at: datetime = strawberry.UNSET

    @strawberry.field
    def applicant_profile(self, info: Info) -> Optional[ApplicantProfileType]:
        from app.crud.applicant_profile import get_profile_by_user
        profile = get_profile_by_user(info.context.db, self.id)
        if not profile:
            return None
        return ApplicantProfileType(
            id=profile.id, user_id=profile.user_id, given_name=profile.given_name,
            middle_name=profile.middle_name, family_name=profile.family_name,
            bio=profile.bio, resume_url=profile.resume_url, portfolio_url=profile.portfolio_url,
            profile_visibility=profile.profile_visibility, hide_applications=profile.hide_applications,
        )


@strawberry.type
class AuthPayload:
    access_token: str
    token_type: str
    user: UserType
