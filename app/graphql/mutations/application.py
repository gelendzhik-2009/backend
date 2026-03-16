"""Application mutations — apply, update status, withdraw"""

import uuid as _uuid
import strawberry
from strawberry.types import Info
from app.graphql.permissions import IsAuthenticated, IsEmployer
from app.graphql.types.application import ApplicationType
from app.graphql.inputs.application import CreateApplicationInput, UpdateApplicationStatusInput


def _app_type(db_app) -> ApplicationType:
    return ApplicationType(
        id=db_app.id, post_id=db_app.post_id, applicant_id=db_app.applicant_id,
        status=db_app.status, cover_letter=db_app.cover_letter,
        created_at=db_app.created_at, updated_at=db_app.updated_at,
    )


@strawberry.type
class ApplicationMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def apply_to_post(self, info: Info, input: CreateApplicationInput) -> ApplicationType:
        from app.crud.application import create_application
        db_app = create_application(
            info.context.db, info.context.user.id,
            input.post_id, input.cover_letter,
        )
        return _app_type(db_app)

    @strawberry.mutation(permission_classes=[IsEmployer])
    def update_application_status(self, info: Info, input: UpdateApplicationStatusInput) -> ApplicationType:
        from app.crud.application import get_application, update_application_status
        db_app = get_application(info.context.db, input.application_id)
        if not db_app:
            raise ValueError("Application not found")
        db_app = update_application_status(info.context.db, db_app, input.status)
        return _app_type(db_app)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def withdraw_application(self, info: Info, application_id: _uuid.UUID) -> bool:
        from app.crud.application import get_application, delete_application
        db_app = get_application(info.context.db, application_id)
        if not db_app or db_app.applicant_id != info.context.user.id:
            raise ValueError("Application not found")
        return delete_application(info.context.db, application_id)
