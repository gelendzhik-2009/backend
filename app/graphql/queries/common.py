"""Common queries — skills, hashtags"""

import strawberry
from strawberry.types import Info
from app.graphql.types.user import SkillType
from app.graphql.types.post import HashtagType


@strawberry.type
class CommonQuery:
    @strawberry.field
    def skills(self, info: Info, skip: int = 0, limit: int = 200) -> list[SkillType]:
        from app.crud.skill import get_skills
        rows = get_skills(info.context.db, skip=skip, limit=limit)
        return [SkillType(id=r.id, name=r.name) for r in rows]

    @strawberry.field
    def hashtags(self, info: Info, skip: int = 0, limit: int = 200) -> list[HashtagType]:
        from app.crud.hashtag import get_hashtags
        rows = get_hashtags(info.context.db, skip=skip, limit=limit)
        return [HashtagType(id=r.id, name=r.name) for r in rows]
