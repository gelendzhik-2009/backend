"""Notification mutations — mark read"""

import uuid as _uuid
import strawberry
from strawberry.types import Info
from app.graphql.permissions import IsAuthenticated


@strawberry.type
class NotificationMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def mark_notification_read(self, info: Info, notification_id: _uuid.UUID) -> bool:
        from app.models.notification import Notification
        db = info.context.db
        db_notif = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == info.context.user.id,
        ).first()
        if not db_notif:
            raise ValueError("Notification not found")
        db_notif.is_read = True
        db.commit()
        return True

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def mark_all_notifications_read(self, info: Info) -> bool:
        from app.crud.notification import mark_all_read
        mark_all_read(info.context.db, info.context.user.id)
        return True
