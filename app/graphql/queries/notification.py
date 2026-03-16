"""Notification queries"""

import strawberry
from strawberry.types import Info
from app.graphql.types.common import NotificationType as NotifType
from app.graphql.permissions import IsAuthenticated


@strawberry.type
class NotificationQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def notifications(self, info: Info, unread_only: bool = False) -> list[NotifType]:
        from app.crud.notification import get_notifications
        rows = get_notifications(info.context.db, info.context.user.id, unread_only=unread_only)
        return [NotifType(
            id=r.id, user_id=r.user_id, type=r.type, title=r.title,
            message=r.message, is_read=r.is_read, reference_id=r.reference_id,
            created_at=r.created_at,
        ) for r in rows]
