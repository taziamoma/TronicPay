from django.urls import path, include
from . import views
import tenant

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("edit-profile/", views.EditProfileView, name="edit-profile"),

]
