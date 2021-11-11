from django.urls import path, include
from. import views

urlpatterns = [
    path("", views.DashboardView, name="dashboard"),
    path("payment/", views.PaymentView, name="payment"),
    path("service-request/", views.ServiceRequestView, name="service-request"),
    path("create-service-request/", views.CreateServiceRequestView, name="create-service-request"),
    path("delete-service-request/<int:pk>", views.DeleteServiceRequestView, name="delete-service-request"),
    path("account-summary/", views.AccountSummaryView, name="account-summary"),
    path("recurring-payment/", views.RecurringPaymentView, name="recurring-payment"),
]
