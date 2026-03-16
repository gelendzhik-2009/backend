"""Input types for application mutations"""

import uuid as _uuid
from typing import Optional
import strawberry


@strawberry.input
class CreateApplicationInput:
    post_id: _uuid.UUID
    cover_letter: Optional[str] = None


@strawberry.input
class UpdateApplicationStatusInput:
    application_id: _uuid.UUID
    status: str
