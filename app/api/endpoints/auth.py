from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.crud.user import create_user, authenticate_user, generate_user_token, get_user_by_email, get_user_by_username
from app.security import create_access_token, get_current_active_user
from app.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    db_user_email = get_user_by_email(db, user.email)
    if db_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user_username = get_user_by_username(db, user.username)
    if db_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    db_user = create_user(db, user)

    # Create access token for the new user
    access_token = generate_user_token(db_user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user
    }


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    db_user = authenticate_user(db, user.username, user.password)
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = generate_user_token(db_user)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user
