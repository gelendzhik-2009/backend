"""Input types for company mutations"""

import uuid as _uuid
from typing import Optional
import strawberry


@strawberry.input
class AddressInput:
    country_code: str
    city: str
    address_line: str
    latitude: float
    longitude: float
    region: Optional[str] = None
    postal_code: Optional[str] = None


@strawberry.input
class CreateCompanyInput:
    name: str
    description: Optional[str] = None
    industry: Optional[str] = None
    website_url: Optional[str] = None
    logo_url: Optional[str] = None
    address: Optional[AddressInput] = None


@strawberry.input
class UpdateCompanyInput:
    name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    website_url: Optional[str] = None
    logo_url: Optional[str] = None


@strawberry.input
class CompanySocialLinkInput:
    platform_name: str
    url: str


@strawberry.input
class CompanyPhotoInput:
    url: str
    sort_order: Optional[int] = None


@strawberry.input
class VerificationRequestInput:
    tax_country_code: Optional[str] = None
    tax_id: Optional[str] = None
