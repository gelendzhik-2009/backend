"""GraphQL types for Notification"""

import uuid as _uuid
from datetime import datetime
from typing import Optional
import strawberry


@strawberry.type
class NotificationType:
    id: _uuid.UUID
    user_id: _uuid.UUID
    type: str
    title: str
    message: Optional[str] = None
    is_read: bool = False
    reference_id: Optional[_uuid.UUID] = None
    created_at: datetime = strawberry.UNSET
