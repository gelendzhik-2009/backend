"""GraphQL types for Contact, Recommendation, Favorite"""

import uuid as _uuid
from datetime import datetime
from typing import Optional
import strawberry


@strawberry.type
class ContactType:
    id: _uuid.UUID
    requester_id: _uuid.UUID
    addressee_id: _uuid.UUID
    status: str
    created_at: datetime = strawberry.UNSET
    updated_at: datetime = strawberry.UNSET


@strawberry.type
class RecommendationType:
    id: _uuid.UUID
    sender_id: _uuid.UUID
    receiver_id: _uuid.UUID
    post_id: _uuid.UUID
    message: Optional[str] = None
    created_at: datetime = strawberry.UNSET


@strawberry.type
class FavoriteType:
    id: _uuid.UUID
    user_id: _uuid.UUID
    post_id: Optional[_uuid.UUID] = None
    company_id: Optional[_uuid.UUID] = None
    created_at: datetime = strawberry.UNSET
