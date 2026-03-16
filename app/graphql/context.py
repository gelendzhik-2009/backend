"""GraphQL request context with DB session and optional current user"""

from typing import Optional, AsyncGenerator
from uuid import UUID
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette.requests import Request
from strawberry.fastapi import BaseContext
from app.config import settings
from app.database import SessionLocal
from app.models.user import User


class Context(BaseContext):
    """Holds DB session and authenticated user for a single GraphQL request"""

    def __init__(self, db: Session, user: Optional[User]):
        self.db = db
        self.user = user


def _extract_user(request: Request, db: Session) -> Optional[User]:
    """Parse Bearer token from request and resolve user"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header[7:]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str = payload.get("sub")
        if user_id_str is None:
            return None
        user_id = UUID(user_id_str)
    except (JWTError, ValueError, TypeError):
        return None
    return db.query(User).filter(User.id == user_id).first()


async def get_context(request: Request) -> AsyncGenerator[Context, None]:
    """Strawberry context dependency — yields context and closes DB session"""
    db = SessionLocal()
    try:
        user = _extract_user(request, db)
        yield Context(db=db, user=user)
    finally:
        db.close()
