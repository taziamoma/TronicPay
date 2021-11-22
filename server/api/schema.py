import strawberry
from typing import List
import strawberry_django
# import strawberry_django.auth as auth

from users.types import User


@strawberry.type
class Query:
    user: User = strawberry_django.field()
    users: List[User] = strawberry_django.field()


schema = strawberry.Schema(query=Query)
