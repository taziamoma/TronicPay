import strawberry_django
from strawberry_django import auto
from .models import CustomUser


@strawberry_django.type(CustomUser)
class User:
    id: auto
    email: auto
    first_name: auto
    last_name: auto
    phone: auto
    address: auto
    city: auto
    state: auto
    zipcode: auto
