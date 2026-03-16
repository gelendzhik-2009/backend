"""Input types for social/contact/favorite/recommendation mutations"""

import uuid as _uuid
from typing import Optional
import strawberry


@strawberry.input
class ContactRequestInput:
    addressee_id: _uuid.UUID


@strawberry.input
class RespondContactInput:
    contact_id: _uuid.UUID
    accept: bool


@strawberry.input
class RecommendationInput:
    receiver_id: _uuid.UUID
    post_id: _uuid.UUID
    message: Optional[str] = None


@strawberry.input
class FavoriteInput:
    post_id: Optional[_uuid.UUID] = None
    company_id: Optional[_uuid.UUID] = None
