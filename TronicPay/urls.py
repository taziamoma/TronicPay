from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("dashboard/", include('tenant.urls')),
    path("", include('users.urls')),
    path("landlord/", include('landlords.urls')),
]
