"""Company mutations"""

import uuid as _uuid
import strawberry
from strawberry.types import Info
from app.graphql.permissions import IsAuthenticated, IsEmployer, IsModerator
from app.graphql.types.company import CompanyType, CompanySocialLinkType, CompanyPhotoType, VerificationRequestType
from app.graphql.inputs.company import (
    CreateCompanyInput, UpdateCompanyInput, CompanySocialLinkInput,
    CompanyPhotoInput, VerificationRequestInput,
)


def _company_type(db_company) -> CompanyType:
    return CompanyType(
        id=db_company.id, owner_id=db_company.owner_id, name=db_company.name,
        description=db_company.description, industry=db_company.industry,
        website_url=db_company.website_url, logo_url=db_company.logo_url,
        is_verified=db_company.is_verified, created_at=db_company.created_at,
        updated_at=db_company.updated_at,
    )


@strawberry.type
class CompanyMutation:
    @strawberry.mutation(permission_classes=[IsEmployer])
    def create_company(self, info: Info, input: CreateCompanyInput) -> CompanyType:
        from app.crud.company import create_company
        from app.crud.address import create_address
        db = info.context.db
        data = {k: v for k, v in vars(input).items() if v is not None and k != "address"}
        if input.address:
            addr = create_address(db, vars(input.address))
            data["address_id"] = addr.id
        db_company = create_company(db, info.context.user.id, data)
        return _company_type(db_company)

    @strawberry.mutation(permission_classes=[IsEmployer])
    def update_company(self, info: Info, company_id: _uuid.UUID, input: UpdateCompanyInput) -> CompanyType:
        from app.crud.company import get_company, update_company
        db_company = get_company(info.context.db, company_id)
        if not db_company or db_company.owner_id != info.context.user.id:
            raise ValueError("Company not found or not owned by you")
        data = {k: v for k, v in vars(input).items() if v is not None}
        db_company = update_company(info.context.db, db_company, data)
        return _company_type(db_company)

    @strawberry.mutation(permission_classes=[IsEmployer])
    def delete_company(self, info: Info, company_id: _uuid.UUID) -> bool:
        from app.crud.company import get_company, delete_company
        db_company = get_company(info.context.db, company_id)
        if not db_company or db_company.owner_id != info.context.user.id:
            raise ValueError("Company not found or not owned by you")
        return delete_company(info.context.db, company_id)

    @strawberry.mutation(permission_classes=[IsEmployer])
    def add_social_link(self, info: Info, company_id: _uuid.UUID, input: CompanySocialLinkInput) -> CompanySocialLinkType:
        from app.models.company_social_link import CompanySocialLink
        from app.crud.company import get_company
        db = info.context.db
        db_company = get_company(db, company_id)
        if not db_company or db_company.owner_id != info.context.user.id:
            raise ValueError("Company not found or not owned by you")
        link = CompanySocialLink(company_id=company_id, platform_name=input.platform_name, url=input.url)
        db.add(link)
        db.commit()
        db.refresh(link)
        return CompanySocialLinkType(id=link.id, platform_name=link.platform_name, url=link.url)

    @strawberry.mutation(permission_classes=[IsEmployer])
    def add_photo(self, info: Info, company_id: _uuid.UUID, input: CompanyPhotoInput) -> CompanyPhotoType:
        from app.models.company_photo import CompanyPhoto
        from app.crud.company import get_company
        db = info.context.db
        db_company = get_company(db, company_id)
        if not db_company or db_company.owner_id != info.context.user.id:
            raise ValueError("Company not found or not owned by you")
        photo = CompanyPhoto(company_id=company_id, url=input.url, sort_order=input.sort_order)
        db.add(photo)
        db.commit()
        db.refresh(photo)
        return CompanyPhotoType(id=photo.id, url=photo.url, sort_order=photo.sort_order)

    @strawberry.mutation(permission_classes=[IsEmployer])
    def submit_verification(self, info: Info, company_id: _uuid.UUID, input: VerificationRequestInput) -> VerificationRequestType:
        from app.crud.verification_request import create_verification_request
        from app.crud.company import get_company
        db_company = get_company(info.context.db, company_id)
        if not db_company or db_company.owner_id != info.context.user.id:
            raise ValueError("Company not found or not owned by you")
        data = {k: v for k, v in vars(input).items() if v is not None}
        req = create_verification_request(info.context.db, company_id, data)
        return VerificationRequestType(
            id=req.id, company_id=req.company_id, tax_country_code=req.tax_country_code,
            tax_id=req.tax_id, status=req.status, created_at=req.created_at,
        )

    @strawberry.mutation(permission_classes=[IsModerator])
    def review_verification(self, info: Info, request_id: _uuid.UUID, approved: bool, reason: str = None) -> VerificationRequestType:
        from app.crud.verification_request import get_verification_request, review_verification
        db = info.context.db
        req = get_verification_request(db, request_id)
        if not req:
            raise ValueError("Verification request not found")
        req = review_verification(db, req, info.context.user.id, approved, reason)
        return VerificationRequestType(
            id=req.id, company_id=req.company_id, tax_country_code=req.tax_country_code,
            tax_id=req.tax_id, status=req.status, reviewed_by=req.reviewed_by,
            reviewed_at=req.reviewed_at, rejection_reason=req.rejection_reason, created_at=req.created_at,
        )
