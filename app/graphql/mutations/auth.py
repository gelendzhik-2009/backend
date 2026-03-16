"""Authentication mutations — register, login"""

import strawberry
from strawberry.types import Info
from app.graphql.inputs.auth import RegisterInput, LoginInput
from app.graphql.types.user import AuthPayload, UserType
from app.enums import UserRole


def _user_type(db_user) -> UserType:
    return UserType(
        id=db_user.id, email=db_user.email, display_name=db_user.display_name,
        role=db_user.role, avatar_url=db_user.avatar_url, is_active=db_user.is_active,
        created_at=db_user.created_at, updated_at=db_user.updated_at,
    )


@strawberry.type
class AuthMutation:
    @strawberry.mutation
    def register(self, info: Info, input: RegisterInput) -> AuthPayload:
        from app.crud.user import create_user, get_user_by_email, generate_user_token
        db = info.context.db

        if input.role not in (UserRole.EMPLOYEE.value, UserRole.EMPLOYER.value):
            raise ValueError("Role must be EMPLOYEE or EMPLOYER")

        if get_user_by_email(db, input.email):
            raise ValueError("Email already registered")

        db_user = create_user(db, input.email, input.display_name, input.password, input.role)
        token = generate_user_token(db_user)
        return AuthPayload(access_token=token, token_type="bearer", user=_user_type(db_user))

    @strawberry.mutation
    def login(self, info: Info, input: LoginInput) -> AuthPayload:
        from app.crud.user import authenticate_user, generate_user_token
        db = info.context.db

        db_user = authenticate_user(db, input.email, input.password)
        if not db_user:
            raise ValueError("Invalid email or password")

        token = generate_user_token(db_user)
        return AuthPayload(access_token=token, token_type="bearer", user=_user_type(db_user))
