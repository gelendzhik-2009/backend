from uuid import UUID
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.project_repository import ProjectRepository


def get_projects(db: Session, profile_id: UUID) -> list[Project]:
    """Get all projects for a profile"""
    return db.query(Project).filter(Project.applicant_profile_id == profile_id).all()


def get_project(db: Session, project_id: UUID) -> Project:
    """Get project by ID"""
    return db.query(Project).filter(Project.id == project_id).first()


def create_project(db: Session, profile_id: UUID, data: dict) -> Project:
    """Create a project"""
    db_proj = Project(applicant_profile_id=profile_id, **data)
    db.add(db_proj)
    db.commit()
    db.refresh(db_proj)
    return db_proj


def update_project(db: Session, db_proj: Project, data: dict) -> Project:
    """Update project fields"""
    for field, value in data.items():
        setattr(db_proj, field, value)
    db.commit()
    db.refresh(db_proj)
    return db_proj


def delete_project(db: Session, project_id: UUID) -> bool:
    """Delete a project"""
    db_proj = db.query(Project).filter(Project.id == project_id).first()
    if db_proj:
        db.delete(db_proj)
        db.commit()
        return True
    return False


def add_repository(db: Session, project_id: UUID, data: dict) -> ProjectRepository:
    """Add repository to a project"""
    db_repo = ProjectRepository(project_id=project_id, **data)
    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)
    return db_repo


def delete_repository(db: Session, repo_id: UUID) -> bool:
    """Delete a project repository"""
    db_repo = db.query(ProjectRepository).filter(ProjectRepository.id == repo_id).first()
    if db_repo:
        db.delete(db_repo)
        db.commit()
        return True
    return False
