from django.urls import path, include
from. import views

urlpatterns = [
    path("", views.LandlordDashView, name="landlord-dash"),
    path("units/", views.UnitsView, name="units"),
    path("tenants/", views.MyTenantsView, name="my-tenants"),
    path("units/new/", views.NewUnitView, name="new-unit"),
    path("units/delete/<str:pk>", views.DeleteUnitView, name="delete-unit"),

]
