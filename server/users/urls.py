from django.urls import path, include
from . import views
import tenant
from strawberry.django.views import GraphQLView
from api.schema import schema

urlpatterns = [
    path("graphql", GraphQLView.as_view(schema=schema)),
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("edit-profile/", views.EditProfileView, name="edit-profile"),

]
