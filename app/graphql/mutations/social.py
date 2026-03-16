"""Social mutations — contacts, recommendations, favorites"""

import uuid as _uuid
import strawberry
from strawberry.types import Info
from app.graphql.permissions import IsAuthenticated
from typing import Optional
from app.graphql.types.social import ContactType, RecommendationType, FavoriteType
from app.graphql.inputs.social import (
    ContactRequestInput, RespondContactInput,
    RecommendationInput, FavoriteInput,
)


@strawberry.type
class SocialMutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def send_contact_request(self, info: Info, input: ContactRequestInput) -> ContactType:
        from app.crud.contact import create_contact_request
        db_c = create_contact_request(info.context.db, info.context.user.id, input.addressee_id)
        return ContactType(
            id=db_c.id, requester_id=db_c.requester_id,
            addressee_id=db_c.addressee_id, status=db_c.status,
            created_at=db_c.created_at, updated_at=db_c.updated_at,
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def respond_to_contact(self, info: Info, input: RespondContactInput) -> ContactType:
        from app.crud.contact import get_contact, respond_to_contact
        db_c = get_contact(info.context.db, input.contact_id)
        if not db_c or db_c.addressee_id != info.context.user.id:
            raise ValueError("Contact request not found")
        new_status = "ACCEPTED" if input.accept else "REJECTED"
        db_c = respond_to_contact(info.context.db, db_c, new_status)
        return ContactType(
            id=db_c.id, requester_id=db_c.requester_id,
            addressee_id=db_c.addressee_id, status=db_c.status,
            created_at=db_c.created_at, updated_at=db_c.updated_at,
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def send_recommendation(self, info: Info, input: RecommendationInput) -> RecommendationType:
        from app.crud.recommendation import create_recommendation
        db_r = create_recommendation(
            info.context.db, info.context.user.id,
            input.receiver_id, input.post_id, input.message,
        )
        return RecommendationType(
            id=db_r.id, sender_id=db_r.sender_id, receiver_id=db_r.receiver_id,
            post_id=db_r.post_id, message=db_r.message, created_at=db_r.created_at,
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def toggle_favorite(self, info: Info, input: FavoriteInput) -> Optional[FavoriteType]:
        if not input.post_id and not input.company_id:
            raise ValueError("Either post_id or company_id must be provided")
        from app.crud.favorite import toggle_favorite
        db_f, created = toggle_favorite(info.context.db, info.context.user.id, input.post_id, input.company_id)
        if not created:
            return None
        return FavoriteType(
            id=db_f.id, user_id=db_f.user_id,
            post_id=db_f.post_id, company_id=db_f.company_id,
            created_at=db_f.created_at,
        )

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    def remove_favorite(self, info: Info, favorite_id: _uuid.UUID) -> bool:
        from app.crud.favorite import remove_favorite
        return remove_favorite(info.context.db, info.context.user.id, favorite_id)
