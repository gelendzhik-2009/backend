"""GraphQL types for Post base and PostContact"""

import uuid as _uuid
from datetime import datetime
from typing import Optional
import strawberry
from strawberry.types import Info
from app.graphql.types.user import SkillType


@strawberry.type
class HashtagType:
    id: int
    name: str


@strawberry.type
class PostContactChannelType:
    id: _uuid.UUID
    type: str
    value: str
    label: Optional[str] = None
    is_primary: Optional[bool] = False


@strawberry.type
class PostContactType:
    id: _uuid.UUID
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website_url: Optional[str] = None
    apply_url: Optional[str] = None
    note: Optional[str] = None

    @strawberry.field
    def channels(self, info: Info) -> list[PostContactChannelType]:
        from app.models.post_contact_channel import PostContactChannel
        rows = info.context.db.query(PostContactChannel).filter(PostContactChannel.post_contact_id == self.id).all()
        return [PostContactChannelType(
            id=r.id, type=r.type, value=r.value, label=r.label, is_primary=r.is_primary,
        ) for r in rows]


@strawberry.type
class PostType:
    id: _uuid.UUID
    author_id: _uuid.UUID
    company_id: _uuid.UUID
    type: str
    status: str
    created_at: datetime = strawberry.UNSET
    updated_at: datetime = strawberry.UNSET
    _skills_cache: strawberry.Private[Optional[list]] = None
    _hashtags_cache: strawberry.Private[Optional[list]] = None

    @strawberry.field
    def contact(self, info: Info) -> Optional[PostContactType]:
        from app.models.post_contact import PostContact
        row = info.context.db.query(PostContact).filter(PostContact.post_id == self.id).first()
        if not row:
            return None
        return PostContactType(
            id=row.id, contact_person=row.contact_person, email=row.email,
            phone=row.phone, website_url=row.website_url, apply_url=row.apply_url, note=row.note,
        )

    @strawberry.field
    def skills(self, info: Info) -> list[SkillType]:
        if self._skills_cache is not None:
            return [SkillType(id=s.id, name=s.name) for s in self._skills_cache]
        from app.models.post import Post
        db_post = info.context.db.query(Post).filter(Post.id == self.id).first()
        return [SkillType(id=s.id, name=s.name) for s in db_post.skills] if db_post else []

    @strawberry.field
    def hashtags(self, info: Info) -> list[HashtagType]:
        if self._hashtags_cache is not None:
            return [HashtagType(id=h.id, name=h.name) for h in self._hashtags_cache]
        from app.models.post import Post
        db_post = info.context.db.query(Post).filter(Post.id == self.id).first()
        return [HashtagType(id=h.id, name=h.name) for h in db_post.hashtags] if db_post else []

    @strawberry.field
    def vacancy(self, info: Info) -> Optional["VacancyPostType"]:
        from app.graphql.types.post_details import load_vacancy
        return load_vacancy(info.context.db, self.id)

    @strawberry.field
    def internship(self, info: Info) -> Optional["InternshipPostType"]:
        from app.graphql.types.post_details import load_internship
        return load_internship(info.context.db, self.id)

    @strawberry.field
    def event(self, info: Info) -> Optional["EventPostType"]:
        from app.graphql.types.post_details import load_event
        return load_event(info.context.db, self.id)

    @strawberry.field
    def mentoring(self, info: Info) -> Optional["MentoringPostType"]:
        from app.graphql.types.post_details import load_mentoring
        return load_mentoring(info.context.db, self.id)

    @strawberry.field
    def simple(self, info: Info) -> Optional["SimplePostType"]:
        from app.graphql.types.post_details import load_simple
        return load_simple(info.context.db, self.id)


from app.graphql.types.post_details import VacancyPostType, InternshipPostType, EventPostType, MentoringPostType, SimplePostType  # noqa: E402
