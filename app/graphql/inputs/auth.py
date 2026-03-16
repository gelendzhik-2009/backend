"""Input types for authentication mutations"""

import strawberry


@strawberry.input
class RegisterInput:
    email: str
    display_name: str
    password: str
    role: str


@strawberry.input
class LoginInput:
    email: str
    password: str
