from sqlalchemy.orm import Session
from app.models.skill import Skill


def get_skill(db: Session, skill_id: int) -> Skill:
    """Get skill by ID"""
    return db.query(Skill).filter(Skill.id == skill_id).first()


def get_skill_by_name(db: Session, name: str) -> Skill:
    """Get skill by name"""
    return db.query(Skill).filter(Skill.name == name).first()


def get_skills(db: Session, skip: int = 0, limit: int = 200) -> list[Skill]:
    """Get all skills"""
    return db.query(Skill).order_by(Skill.name).offset(skip).limit(limit).all()


def create_skill(db: Session, name: str) -> Skill:
    """Create a new skill"""
    db_skill = Skill(name=name)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill


def delete_skill(db: Session, skill_id: int) -> bool:
    """Delete a skill"""
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if db_skill:
        db.delete(db_skill)
        db.commit()
        return True
    return False
