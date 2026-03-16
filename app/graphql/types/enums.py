"""Strawberry enum types mirroring app.enums"""

import enum
import strawberry


@strawberry.enum
class UserRoleGQL(enum.Enum):
    EMPLOYEE = "EMPLOYEE"
    EMPLOYER = "EMPLOYER"
    MODERATOR = "MODERATOR"
    SUPERADMIN = "SUPERADMIN"


@strawberry.enum
class PostTypeGQL(enum.Enum):
    VACANCY = "VACANCY"
    INTERNSHIP = "INTERNSHIP"
    EVENT = "EVENT"
    MENTORING_PROGRAM = "MENTORING_PROGRAM"
    POST = "POST"


@strawberry.enum
class WorkFormatGQL(enum.Enum):
    OFFICE = "OFFICE"
    HYBRID = "HYBRID"
    REMOTE = "REMOTE"


@strawberry.enum
class EmploymentTypeGQL(enum.Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    PROJECT = "PROJECT"


@strawberry.enum
class CompensationPeriodGQL(enum.Enum):
    HOURLY = "HOURLY"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    TOTAL = "TOTAL"


@strawberry.enum
class ExperienceLevelGQL(enum.Enum):
    INTERN = "INTERN"
    JUNIOR = "JUNIOR"
    MIDDLE = "MIDDLE"
    SENIOR = "SENIOR"


@strawberry.enum
class PostStatusGQL(enum.Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    PLANNED = "PLANNED"


@strawberry.enum
class ApplicationStatusGQL(enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    RESERVED = "RESERVED"


@strawberry.enum
class ContactStatusGQL(enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


@strawberry.enum
class ContactChannelTypeGQL(enum.Enum):
    TELEGRAM = "TELEGRAM"
    WHATSAPP = "WHATSAPP"
    MAX = "MAX"
    VK = "VK"
    FACEBOOK_MESSENGER = "FACEBOOK_MESSENGER"
    SLACK = "SLACK"
    LINKEDIN = "LINKEDIN"


@strawberry.enum
class VerificationStatusGQL(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


@strawberry.enum
class NotificationTypeGQL(enum.Enum):
    COMPANY = "COMPANY"
    RECOMMENDATION = "RECOMMENDATION"
    APPLICATION_STATUS = "APPLICATION_STATUS"
    CONTACT_REQUEST = "CONTACT_REQUEST"
    SYSTEM = "SYSTEM"


@strawberry.enum
class PrivacyLevelGQL(enum.Enum):
    PRIVATE = "PRIVATE"
    CONTACTS_ONLY = "CONTACTS_ONLY"
    PUBLIC = "PUBLIC"
