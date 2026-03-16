"""Post mutations — create, update, delete posts with detail tables"""

import uuid as _uuid
import strawberry
from strawberry.types import Info
from app.graphql.permissions import IsEmployer
from app.graphql.types.post import PostType
from app.graphql.inputs.post import CreatePostInput


def _post_type(db_post) -> PostType:
    return PostType(
        id=db_post.id, author_id=db_post.author_id, company_id=db_post.company_id,
        type=db_post.type, status=db_post.status,
        created_at=db_post.created_at, updated_at=db_post.updated_at,
    )


def _create_address(db, addr_input):
    from app.crud.address import create_address
    return create_address(db, vars(addr_input))


def _attach_contact(db, post_id, contact_input):
    from app.models.post_contact import PostContact
    from app.models.post_contact_channel import PostContactChannel
    data = {k: v for k, v in vars(contact_input).items() if k != "channels" and v is not None}
    pc = PostContact(post_id=post_id, **data)
    db.add(pc)
    db.flush()
    for ch in (contact_input.channels or []):
        db.add(PostContactChannel(post_contact_id=pc.id, type=ch.type, value=ch.value, label=ch.label, is_primary=ch.is_primary))


def _attach_skills_hashtags(db, db_post, skill_ids, hashtag_ids):
    from app.models.skill import Skill
    from app.models.hashtag import Hashtag
    if skill_ids:
        skills = db.query(Skill).filter(Skill.id.in_(skill_ids)).all()
        db_post.skills = skills
    if hashtag_ids:
        tags = db.query(Hashtag).filter(Hashtag.id.in_(hashtag_ids)).all()
        db_post.hashtags = tags


@strawberry.type
class PostMutation:
    @strawberry.mutation(permission_classes=[IsEmployer])
    def create_post(self, info: Info, input: CreatePostInput) -> PostType:
        from app.crud.post import create_post
        from app.crud.company import get_company
        db = info.context.db
        db_company = get_company(db, input.company_id)
        if not db_company or db_company.owner_id != info.context.user.id:
            raise ValueError("Company not found or not owned by you")

        db_post = create_post(db, info.context.user.id, input.company_id, input.post_type)

        if input.contact:
            _attach_contact(db, db_post.id, input.contact)

        _create_detail(db, db_post, input)
        _attach_skills_hashtags(db, db_post, input.skill_ids, input.hashtag_ids)

        db.commit()
        db.refresh(db_post)
        return _post_type(db_post)

    @strawberry.mutation(permission_classes=[IsEmployer])
    def update_post_status(self, info: Info, post_id: _uuid.UUID, status: str) -> PostType:
        from app.crud.post import get_post, update_post
        db_post = get_post(info.context.db, post_id)
        if not db_post or db_post.author_id != info.context.user.id:
            raise ValueError("Post not found or not authored by you")
        db_post = update_post(info.context.db, db_post, {"status": status})
        return _post_type(db_post)

    @strawberry.mutation(permission_classes=[IsEmployer])
    def delete_post(self, info: Info, post_id: _uuid.UUID) -> bool:
        from app.crud.post import get_post, delete_post
        db_post = get_post(info.context.db, post_id)
        if not db_post or db_post.author_id != info.context.user.id:
            raise ValueError("Post not found or not authored by you")
        return delete_post(info.context.db, post_id)

    @strawberry.mutation(permission_classes=[IsEmployer])
    def add_skill_to_post(self, info: Info, post_id: _uuid.UUID, skill_id: int) -> bool:
        from app.crud.post import get_post
        from app.crud.skill import get_skill
        db = info.context.db
        db_post = get_post(db, post_id)
        if not db_post or db_post.author_id != info.context.user.id:
            raise ValueError("Post not found or not authored by you")
        skill = get_skill(db, skill_id)
        if not skill:
            raise ValueError("Skill not found")
        if skill not in db_post.skills:
            db_post.skills.append(skill)
            db.commit()
        return True

    @strawberry.mutation(permission_classes=[IsEmployer])
    def add_hashtag_to_post(self, info: Info, post_id: _uuid.UUID, hashtag_id: int) -> bool:
        from app.crud.post import get_post
        from app.crud.hashtag import get_hashtag
        db = info.context.db
        db_post = get_post(db, post_id)
        if not db_post or db_post.author_id != info.context.user.id:
            raise ValueError("Post not found or not authored by you")
        tag = get_hashtag(db, hashtag_id)
        if not tag:
            raise ValueError("Hashtag not found")
        if tag not in db_post.hashtags:
            db_post.hashtags.append(tag)
            db.commit()
        return True


def _create_detail(db, db_post, input: CreatePostInput):
    if input.vacancy:
        from app.models.vacancy_post import VacancyPost
        addr = _create_address(db, input.vacancy.address)
        data = {k: v for k, v in vars(input.vacancy).items() if k != "address" and v is not None}
        db.add(VacancyPost(post_id=db_post.id, address_id=addr.id, **data))

    elif input.internship:
        from app.models.internship_post import InternshipPost
        addr = _create_address(db, input.internship.address)
        data = {k: v for k, v in vars(input.internship).items() if k != "address" and v is not None}
        db.add(InternshipPost(post_id=db_post.id, address_id=addr.id, **data))

    elif input.event:
        from app.models.event_post import EventPost
        data = {k: v for k, v in vars(input.event).items() if k != "address" and v is not None}
        if input.event.address:
            addr = _create_address(db, input.event.address)
            data["address_id"] = addr.id
        db.add(EventPost(post_id=db_post.id, **data))

    elif input.mentoring:
        from app.models.mentoring_post import MentoringPost
        data = {k: v for k, v in vars(input.mentoring).items() if k != "address" and v is not None}
        if input.mentoring.address:
            addr = _create_address(db, input.mentoring.address)
            data["address_id"] = addr.id
        db.add(MentoringPost(post_id=db_post.id, **data))

    elif input.simple:
        from app.models.simple_post import SimplePost
        db.add(SimplePost(post_id=db_post.id, description=input.simple.description, image_url=input.simple.image_url))
