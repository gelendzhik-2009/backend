"""GraphQL types for Company, CompanySocialLink, CompanyPhoto, VerificationRequest"""

import uuid as _uuid
from datetime import datetime
from typing import Optional
import strawberry
from strawberry.types import Info


@strawberry.type
class CompanySocialLinkType:
    id: _uuid.UUID
    platform_name: str
    url: str


@strawberry.type
class CompanyPhotoType:
    id: _uuid.UUID
    url: str
    sort_order: Optional[int] = None


@strawberry.type
class VerificationRequestType:
    id: _uuid.UUID
    company_id: _uuid.UUID
    tax_country_code: Optional[str] = None
    tax_id: Optional[str] = None
    status: str = "PENDING"
    reviewed_by: Optional[_uuid.UUID] = None
    reviewed_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    created_at: datetime = strawberry.UNSET


@strawberry.type
class AddressType:
    id: _uuid.UUID
    country_code: str
    region: Optional[str] = None
    city: str
    postal_code: Optional[str] = None
    address_line: str
    latitude: float
    longitude: float


@strawberry.type
class CompanyType:
    id: _uuid.UUID
    owner_id: _uuid.UUID
    name: str
    description: Optional[str] = None
    industry: Optional[str] = None
    website_url: Optional[str] = None
    logo_url: Optional[str] = None
    is_verified: bool = False
    created_at: datetime = strawberry.UNSET
    updated_at: datetime = strawberry.UNSET

    @strawberry.field
    def address(self, info: Info) -> Optional[AddressType]:
        from app.models.company import Company
        db_company = info.context.db.query(Company).filter(Company.id == self.id).first()
        if not db_company or not db_company.address:
            return None
        addr = db_company.address
        return AddressType(
            id=addr.id, country_code=addr.country_code, region=addr.region,
            city=addr.city, postal_code=addr.postal_code, address_line=addr.address_line,
            latitude=float(addr.latitude), longitude=float(addr.longitude),
        )

    @strawberry.field
    def social_links(self, info: Info) -> list[CompanySocialLinkType]:
        from app.models.company_social_link import CompanySocialLink
        rows = info.context.db.query(CompanySocialLink).filter(CompanySocialLink.company_id == self.id).all()
        return [CompanySocialLinkType(id=r.id, platform_name=r.platform_name, url=r.url) for r in rows]

    @strawberry.field
    def photos(self, info: Info) -> list[CompanyPhotoType]:
        from app.models.company_photo import CompanyPhoto
        rows = info.context.db.query(CompanyPhoto).filter(CompanyPhoto.company_id == self.id).all()
        return [CompanyPhotoType(id=r.id, url=r.url, sort_order=r.sort_order) for r in rows]

    @strawberry.field
    def verification_requests(self, info: Info) -> list[VerificationRequestType]:
        from app.models.verification_request import VerificationRequest
        rows = info.context.db.query(VerificationRequest).filter(VerificationRequest.company_id == self.id).all()
        return [VerificationRequestType(
            id=r.id, company_id=r.company_id, tax_country_code=r.tax_country_code,
            tax_id=r.tax_id, status=r.status, reviewed_by=r.reviewed_by,
            reviewed_at=r.reviewed_at, rejection_reason=r.rejection_reason, created_at=r.created_at,
        ) for r in rows]
