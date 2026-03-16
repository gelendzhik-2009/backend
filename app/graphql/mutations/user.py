"""User and applicant profile mutations"""

import uuid as _uuid
import strawberry
from strawberry.types import Info
from app.graphql.permissions import IsAuthenticated
from app.graphql.types.user import UserType, ApplicantProfileType, EducationType, ProjectType
from app.graphql.inputs.user import (
    UpdateUserInput, UpdateApplicantProfileInput,
    EducationInput, ProjectInput, ProjectRepositoryInput,
)


def _user_type(db_user) -> UserType:
    return UserType(
        id=db_user.id, email=db_user.email, display_name=db_user.display_name,
        role=db_user.role, avatar_url=db_user.avatar_url, is_active=db_user.is_active,
        created_at=db_user.created_at, updated_at=db_user.updated_at,
    )


def _profile_type(profile) -> ApplicantProfileType:
    return ApplicantProfileType(
        id=profile.id, user_id=profile.user_id, given_name=profile.given_name,
        middle_name=profile.middle_name, family_name=profile.family_name,
        bio=profile.bio, resume_url=profile.resume_url, portfolio_url=profile.portfolio_url,
        profile_visibility=profile.profile_visibility, hide_applications=profile.hide_applications,
    )


@strawberry.type
class UserMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_user(self, info: Info, input: UpdateUserInput) -> UserType:
        from app.crud.user import update_user
        data = {k: v for k, v in vars(input).items() if v is not None}
        db_user = update_user(info.context.db, info.context.user, data)
        return _user_type(db_user)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def update_applicant_profile(self, info: Info, input: UpdateApplicantProfileInput) -> ApplicantProfileType:
        from app.crud.applicant_profile import get_profile_by_user, create_profile, update_profile
        db = info.context.db
        data = {k: v for k, v in vars(input).items() if v is not None}
        profile = get_profile_by_user(db, info.context.user.id)
        if profile:
            profile = update_profile(db, profile, data)
        else:
            profile = create_profile(db, info.context.user.id, data)
        return _profile_type(profile)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def add_education(self, info: Info, input: EducationInput) -> EducationType:
        from app.crud.applicant_profile import get_profile_by_user
        from app.crud.education import create_education
        profile = get_profile_by_user(info.context.db, info.context.user.id)
        if not profile:
            raise ValueError("Create applicant profile first")
        edu = create_education(info.context.db, profile.id, vars(input))
        return EducationType(
            id=edu.id, organization_name=edu.organization_name, degree=edu.degree,
            field_of_study=edu.field_of_study, start_year=edu.start_year,
            graduation_year=edu.graduation_year, is_current=edu.is_current,
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def delete_education(self, info: Info, education_id: _uuid.UUID) -> bool:
        from app.crud.education import delete_education
        return delete_education(info.context.db, education_id)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def add_project(self, info: Info, input: ProjectInput) -> ProjectType:
        from app.crud.applicant_profile import get_profile_by_user
        from app.crud.project import create_project
        profile = get_profile_by_user(info.context.db, info.context.user.id)
        if not profile:
            raise ValueError("Create applicant profile first")
        proj = create_project(info.context.db, profile.id, vars(input))
        return ProjectType(
            id=proj.id, title=proj.title, description=proj.description,
            role_name=proj.role_name, project_url=proj.project_url,
            demo_url=proj.demo_url, start_date=proj.start_date,
            end_date=proj.end_date, is_ongoing=proj.is_ongoing,
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def delete_project(self, info: Info, project_id: _uuid.UUID) -> bool:
        from app.crud.project import delete_project
        return delete_project(info.context.db, project_id)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def add_skill_to_profile(self, info: Info, skill_id: int) -> bool:
        from app.crud.applicant_profile import get_profile_by_user
        from app.crud.skill import get_skill
        db = info.context.db
        profile = get_profile_by_user(db, info.context.user.id)
        skill = get_skill(db, skill_id)
        if not profile or not skill:
            raise ValueError("Profile or skill not found")
        if skill not in profile.skills:
            profile.skills.append(skill)
            db.commit()
        return True
