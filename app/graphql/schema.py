"""Root GraphQL schema — merges all queries and mutations"""

import strawberry
from app.graphql.queries.user import UserQuery
from app.graphql.queries.company import CompanyQuery
from app.graphql.queries.post import PostQuery
from app.graphql.queries.application import ApplicationQuery
from app.graphql.queries.social import SocialQuery
from app.graphql.queries.notification import NotificationQuery
from app.graphql.queries.common import CommonQuery
from app.graphql.mutations.auth import AuthMutation
from app.graphql.mutations.user import UserMutation
from app.graphql.mutations.company import CompanyMutation
from app.graphql.mutations.post import PostMutation
from app.graphql.mutations.application import ApplicationMutation
from app.graphql.mutations.social import SocialMutation
from app.graphql.mutations.notification import NotificationMutation


@strawberry.type
class Query(
    UserQuery, CompanyQuery, PostQuery, ApplicationQuery,
    SocialQuery, NotificationQuery, CommonQuery,
):
    """Root query — all domain queries merged via inheritance"""


@strawberry.type
class Mutation(
    AuthMutation, UserMutation, CompanyMutation, PostMutation,
    ApplicationMutation, SocialMutation, NotificationMutation,
):
    """Root mutation — all domain mutations merged via inheritance"""


schema = strawberry.Schema(query=Query, mutation=Mutation)
