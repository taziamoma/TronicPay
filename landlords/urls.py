from django.urls import path, include
from. import views

urlpatterns = [
    path("units/", views.UnitsView, name="units"),
    path("tenants/", views.MyTenantsView, name="my-tenants"),
    path("units/new/", views.NewUnitView, name="new-unit"),
    path("units/delete/<str:pk>", views.DeleteUnitView, name="delete-unit"),
    path("units/add-tenant/<str:pk>", views.AddTenantToUnit, name="add-tenant-to-unit"),
    path("units/unit/<str:pk>", views.UnitDetailView, name="view-unit"),

]
