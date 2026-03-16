from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session
from app.models.post import Post


def get_post(db: Session, post_id: UUID) -> Post:
    """Get post by ID"""
    return db.query(Post).filter(Post.id == post_id).first()


def get_posts(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    post_type: Optional[str] = None,
    status: Optional[str] = None,
    company_id: Optional[UUID] = None,
) -> list[Post]:
    """Get posts with optional filters"""
    query = db.query(Post)
    if post_type:
        query = query.filter(Post.type == post_type)
    if status:
        query = query.filter(Post.status == status)
    if company_id:
        query = query.filter(Post.company_id == company_id)
    return query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()


def create_post(db: Session, author_id: UUID, company_id: UUID, post_type: str, status: str = "ACTIVE") -> Post:
    """Create base post record"""
    db_post = Post(author_id=author_id, company_id=company_id, type=post_type, status=status)
    db.add(db_post)
    db.flush()
    return db_post


def update_post(db: Session, db_post: Post, data: dict) -> Post:
    """Update base post fields"""
    for field, value in data.items():
        setattr(db_post, field, value)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: UUID) -> bool:
    """Delete post and cascaded detail"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False
