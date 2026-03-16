"""Social queries — contacts, recommendations, favorites"""

import strawberry
from strawberry.types import Info
from app.graphql.types.social import ContactType, RecommendationType, FavoriteType
from app.graphql.permissions import IsAuthenticated


@strawberry.type
class SocialQuery:
    @strawberry.field(permission_classes=[IsAuthenticated])
    def contacts(self, info: Info) -> list[ContactType]:
        from app.crud.contact import get_contacts_for_user
        rows = get_contacts_for_user(info.context.db, info.context.user.id)
        return [ContactType(
            id=r.id, requester_id=r.requester_id, addressee_id=r.addressee_id,
            status=r.status, created_at=r.created_at, updated_at=r.updated_at,
        ) for r in rows]

    @strawberry.field(permission_classes=[IsAuthenticated])
    def recommendations(self, info: Info) -> list[RecommendationType]:
        from app.crud.recommendation import get_recommendations_for_user
        rows = get_recommendations_for_user(info.context.db, info.context.user.id)
        return [RecommendationType(
            id=r.id, sender_id=r.sender_id, receiver_id=r.receiver_id,
            post_id=r.post_id, message=r.message, created_at=r.created_at,
        ) for r in rows]

    @strawberry.field(permission_classes=[IsAuthenticated])
    def favorites(self, info: Info) -> list[FavoriteType]:
        from app.crud.favorite import get_favorites_by_user
        rows = get_favorites_by_user(info.context.db, info.context.user.id)
        return [FavoriteType(
            id=r.id, user_id=r.user_id, post_id=r.post_id,
            company_id=r.company_id, created_at=r.created_at,
        ) for r in rows]
