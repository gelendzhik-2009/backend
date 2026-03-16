from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.user import User
from app.enums import UserRole

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="graphql", auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def decode_token_to_user_id(token: str) -> UUID:
    """Decode JWT token and return user UUID, raises on failure"""
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise ValueError("Missing sub claim")
    return UUID(user_id_str)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Get current user from token, returns None if unauthenticated"""
    if token is None:
        return None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = decode_token_to_user_id(token)
    except (JWTError, ValueError):
        raise credentials_exception

    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise credentials_exception
    return db_user


def get_current_active_user(
    current_user: Optional[User] = Depends(get_current_user),
) -> User:
    """Require an active authenticated user"""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


def get_current_employer(current_user: User = Depends(get_current_active_user)) -> User:
    """Require EMPLOYER role"""
    if current_user.role != UserRole.EMPLOYER.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Employer access required")
    return current_user


def get_current_moderator(current_user: User = Depends(get_current_active_user)) -> User:
    """Require MODERATOR or SUPERADMIN role"""
    if current_user.role not in (UserRole.MODERATOR.value, UserRole.SUPERADMIN.value):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Moderator access required")
    return current_user


def get_current_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """Require SUPERADMIN role"""
    if current_user.role != UserRole.SUPERADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user
