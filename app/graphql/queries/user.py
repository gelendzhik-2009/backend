"""User queries"""

import uuid as _uuid
from typing import Optional
import strawberry
from strawberry.types import Info
from app.graphql.types.user import UserType, ApplicantProfileType
from app.graphql.permissions import IsAuthenticated


def _user_to_type(db_user) -> UserType:
    return UserType(
        id=db_user.id, email=db_user.email, display_name=db_user.display_name,
        role=db_user.role, avatar_url=db_user.avatar_url, is_active=db_user.is_active,
        created_at=db_user.created_at, updated_at=db_user.updated_at,
    )


@strawberry.type
class UserQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def me(self, info: Info) -> UserType:
        return _user_to_type(info.context.user)

    @strawberry.field(permission_classes=[IsAuthenticated])
    def user(self, info: Info, user_id: _uuid.UUID) -> Optional[UserType]:
        from app.crud.user import get_user
        db_user = get_user(info.context.db, user_id)
        return _user_to_type(db_user) if db_user else None

    @strawberry.field(permission_classes=[IsAuthenticated])
    def users(self, info: Info, skip: int = 0, limit: int = 100) -> list[UserType]:
        from app.crud.user import get_users
        rows = get_users(info.context.db, skip=skip, limit=limit)
        return [_user_to_type(r) for r in rows]
