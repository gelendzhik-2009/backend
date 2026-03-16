"""Application queries"""

import uuid as _uuid
import strawberry
from strawberry.types import Info
from app.graphql.types.application import ApplicationType
from app.graphql.permissions import IsAuthenticated


def _app_to_type(db_app) -> ApplicationType:
    return ApplicationType(
        id=db_app.id, post_id=db_app.post_id, applicant_id=db_app.applicant_id,
        status=db_app.status, cover_letter=db_app.cover_letter,
        created_at=db_app.created_at, updated_at=db_app.updated_at,
    )


@strawberry.type
class ApplicationQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def my_applications(self, info: Info) -> list[ApplicationType]:
        from app.crud.application import get_applications_by_user
        rows = get_applications_by_user(info.context.db, info.context.user.id)
        return [_app_to_type(r) for r in rows]

    @strawberry.field(permission_classes=[IsAuthenticated])
    def applications_for_post(self, info: Info, post_id: _uuid.UUID) -> list[ApplicationType]:
        from app.crud.application import get_applications_by_post
        rows = get_applications_by_post(info.context.db, post_id)
        return [_app_to_type(r) for r in rows]
