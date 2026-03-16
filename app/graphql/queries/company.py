"""Company queries"""

import uuid as _uuid
from typing import Optional
import strawberry
from strawberry.types import Info
from app.graphql.types.company import CompanyType, VerificationRequestType
from app.graphql.permissions import IsAuthenticated, IsModerator


def _company_to_type(db_company) -> CompanyType:
    return CompanyType(
        id=db_company.id, owner_id=db_company.owner_id, name=db_company.name,
        description=db_company.description, industry=db_company.industry,
        website_url=db_company.website_url, logo_url=db_company.logo_url,
        is_verified=db_company.is_verified, created_at=db_company.created_at,
        updated_at=db_company.updated_at,
    )


@strawberry.type
class CompanyQuery:
    @strawberry.field
    def company(self, info: Info, company_id: _uuid.UUID) -> Optional[CompanyType]:
        from app.crud.company import get_company
        db_company = get_company(info.context.db, company_id)
        return _company_to_type(db_company) if db_company else None

    @strawberry.field
    def companies(self, info: Info, skip: int = 0, limit: int = 100) -> list[CompanyType]:
        from app.crud.company import get_companies
        rows = get_companies(info.context.db, skip=skip, limit=limit)
        return [_company_to_type(r) for r in rows]

    @strawberry.field(permission_classes=[IsAuthenticated])
    def my_companies(self, info: Info) -> list[CompanyType]:
        from app.crud.company import get_companies_by_owner
        rows = get_companies_by_owner(info.context.db, info.context.user.id)
        return [_company_to_type(r) for r in rows]

    @strawberry.field(permission_classes=[IsModerator])
    def pending_verifications(self, info: Info, skip: int = 0, limit: int = 50) -> list[VerificationRequestType]:
        from app.crud.verification_request import get_pending_requests
        rows = get_pending_requests(info.context.db, skip=skip, limit=limit)
        return [VerificationRequestType(
            id=r.id, company_id=r.company_id, tax_country_code=r.tax_country_code,
            tax_id=r.tax_id, status=r.status, reviewed_by=r.reviewed_by,
            reviewed_at=r.reviewed_at, rejection_reason=r.rejection_reason, created_at=r.created_at,
        ) for r in rows]
