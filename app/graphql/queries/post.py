"""Post queries"""

import uuid as _uuid
from typing import Optional
import strawberry
from strawberry.types import Info
from app.graphql.types.post import PostType


def _post_to_type(db_post) -> PostType:
    return PostType(
        id=db_post.id, author_id=db_post.author_id, company_id=db_post.company_id,
        type=db_post.type, status=db_post.status,
        created_at=db_post.created_at, updated_at=db_post.updated_at,
        _skills_cache=list(db_post.skills) if hasattr(db_post, 'skills') else None,
        _hashtags_cache=list(db_post.hashtags) if hasattr(db_post, 'hashtags') else None,
    )


@strawberry.type
class PostQuery:
    @strawberry.field
    def post(self, info: Info, post_id: _uuid.UUID) -> Optional[PostType]:
        from app.crud.post import get_post
        db_post = get_post(info.context.db, post_id)
        return _post_to_type(db_post) if db_post else None

    @strawberry.field
    def posts(
        self,
        info: Info,
        skip: int = 0,
        limit: int = 50,
        post_type: Optional[str] = None,
        status: Optional[str] = None,
        company_id: Optional[_uuid.UUID] = None,
    ) -> list[PostType]:
        from app.crud.post import get_posts
        rows = get_posts(
            info.context.db, skip=skip, limit=limit,
            post_type=post_type, status=status, company_id=company_id,
        )
        return [_post_to_type(r) for r in rows]
