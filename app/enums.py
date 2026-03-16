"""Application-wide enumerations matching ERD definitions"""

import enum


class UserRole(str, enum.Enum):
    """User role in the platform"""
    EMPLOYEE = "EMPLOYEE"
    EMPLOYER = "EMPLOYER"
    MODERATOR = "MODERATOR"
    SUPERADMIN = "SUPERADMIN"


class PostType(str, enum.Enum):
    """Type of post/opportunity"""
    VACANCY = "VACANCY"
    INTERNSHIP = "INTERNSHIP"
    EVENT = "EVENT"
    MENTORING_PROGRAM = "MENTORING_PROGRAM"
    POST = "POST"


class WorkFormat(str, enum.Enum):
    """Work format for positions"""
    OFFICE = "OFFICE"
    HYBRID = "HYBRID"
    REMOTE = "REMOTE"


class EmploymentType(str, enum.Enum):
    """Employment type"""
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    PROJECT = "PROJECT"


class CompensationPeriod(str, enum.Enum):
    """Period for salary/compensation"""
    HOURLY = "HOURLY"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"
    TOTAL = "TOTAL"


class ExperienceLevel(str, enum.Enum):
    """Required experience level"""
    INTERN = "INTERN"
    JUNIOR = "JUNIOR"
    MIDDLE = "MIDDLE"
    SENIOR = "SENIOR"


class PostStatus(str, enum.Enum):
    """Publication status of a post"""
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    PLANNED = "PLANNED"


class ApplicationStatus(str, enum.Enum):
    """Status of an applicant's application"""
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    RESERVED = "RESERVED"


class ContactStatus(str, enum.Enum):
    """Status of a contact request between applicants"""
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class ContactChannelType(str, enum.Enum):
    """Messenger/contact channel type"""
    TELEGRAM = "TELEGRAM"
    WHATSAPP = "WHATSAPP"
    MAX = "MAX"
    VK = "VK"
    FACEBOOK_MESSENGER = "FACEBOOK_MESSENGER"
    SLACK = "SLACK"
    LINKEDIN = "LINKEDIN"


class VerificationStatus(str, enum.Enum):
    """Company verification status"""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class NotificationType(str, enum.Enum):
    """Notification category"""
    COMPANY = "COMPANY"
    RECOMMENDATION = "RECOMMENDATION"
    APPLICATION_STATUS = "APPLICATION_STATUS"
    CONTACT_REQUEST = "CONTACT_REQUEST"
    SYSTEM = "SYSTEM"


class PrivacyLevel(str, enum.Enum):
    """Profile visibility level"""
    PRIVATE = "PRIVATE"
    CONTACTS_ONLY = "CONTACTS_ONLY"
    PUBLIC = "PUBLIC"
