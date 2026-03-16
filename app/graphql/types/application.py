"""GraphQL types for Application"""

import uuid as _uuid
from datetime import datetime
from typing import Optional
import strawberry


@strawberry.type
class ApplicationType:
    id: _uuid.UUID
    post_id: _uuid.UUID
    applicant_id: _uuid.UUID
    status: str
    cover_letter: Optional[str] = None
    created_at: datetime = strawberry.UNSET
    updated_at: datetime = strawberry.UNSET
