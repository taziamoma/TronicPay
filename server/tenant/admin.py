from django.contrib import admin
from .models import Invoice, BankAccounts, ServiceRequests, ScheduledPayments, Payments

admin.site.register(Invoice)
admin.site.register(Payments)
admin.site.register(ScheduledPayments)
admin.site.register(BankAccounts)
admin.site.register(ServiceRequests)
