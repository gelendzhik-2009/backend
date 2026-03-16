"""Notification mutations — mark read"""

import uuid as _uuid
import strawberry
from strawberry.types import Info
from app.graphql.permissions import IsAuthenticated


@strawberry.type
class NotificationMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def mark_notification_read(self, info: Info, notification_id: _uuid.UUID) -> bool:
        from app.crud.notification import mark_notification_read
        return mark_notification_read(info.context.db, notification_id)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def mark_all_notifications_read(self, info: Info) -> bool:
        from app.crud.notification import mark_all_read
        return mark_all_read(info.context.db, info.context.user.id)
