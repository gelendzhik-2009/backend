"""Strawberry permission classes for role-based access control"""

import strawberry
from strawberry.permission import BasePermission
from strawberry.types import Info
from app.enums import UserRole


class IsAuthenticated(BasePermission):
    """Require any authenticated user"""
    message = "Authentication required"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        return info.context.user is not None


class IsEmployee(BasePermission):
    """Require EMPLOYEE role"""
    message = "Employee access required"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        user = info.context.user
        return user is not None and user.role == UserRole.EMPLOYEE.value


class IsEmployer(BasePermission):
    """Require EMPLOYER role"""
    message = "Employer access required"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        user = info.context.user
        return user is not None and user.role == UserRole.EMPLOYER.value


class IsModerator(BasePermission):
    """Require MODERATOR or SUPERADMIN role"""
    message = "Moderator access required"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        user = info.context.user
        if user is None:
            return False
        return user.role in (UserRole.MODERATOR.value, UserRole.SUPERADMIN.value)


class IsAdmin(BasePermission):
    """Require SUPERADMIN role"""
    message = "Admin access required"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        user = info.context.user
        return user is not None and user.role == UserRole.SUPERADMIN.value
