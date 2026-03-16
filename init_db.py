"""Initialization script — creates all tables from models"""

from app.database import engine, Base
from app.models import (
    User, ApplicantProfile, Education, Project, ProjectRepository,
    Company, CompanySocialLink, CompanyPhoto, VerificationRequest, Address,
    Post, PostContact, PostContactChannel,
    VacancyPost, InternshipPost, EventPost, MentoringPost, SimplePost,
    Skill, Hashtag, Application, Favorite, Contact, Recommendation, Notification,
)
from app.models.associations import post_skills, post_hashtags, applicant_skills, project_skills

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")
