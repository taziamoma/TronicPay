from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from users.common import CustomUser, Tenancy, Unit

#for importing the settings.AUTH_USER_MODEL
from django.conf import settings
CustomUser = settings.AUTH_USER_MODEL

class Invoice(models.Model):
    ACH = 'ACH'
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'
    TYPE_CHOICES = [
        (ACH, 'ACH'),
        (DEBIT, 'DEBIT'),
        (CREDIT, 'CREDIT')
    ]
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    STATUS_CHOICES = [
        (PENDING, 'PENDING'),
        (COMPLETED, 'COMPLETED')
    ]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=6, choices=TYPE_CHOICES, null=True, blank=True)
    amount_total = models.FloatField(null=True, blank=True, default=0.0)
    amount_paid = models.FloatField(null=True, blank=True, default=0.0)
    due_date = models.DateTimeField()
    date_paid = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True, default=timezone.now)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, null=True, blank=True, default=PENDING)
    scheduled_pay_date = models.DateTimeField(null=True, blank=True)
    tenant = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='invoices')

    def __str__(self):
        return str(self.id) + " - " + str(self.tenant)

class ScheduledPayments(models.Model):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    STATUS_CHOICES = [
        (PENDING, 'PENDING'),
        (PROCESSING, 'PROCESSING'),
        (COMPLETED, 'COMPLETED')
    ]

    id = models.AutoField(primary_key=True)
    amount_to_pay = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True, default=timezone.now)
    date_scheduled = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, related_name='invoice')
    tenant = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='tenant')

    def __str__(self):
        return str(self.id) + " - " + str(self.tenant)

class Payments(models.Model):
    BANK_ACCOUNT = 'ACH'
    DEBIT_CARD = 'DEBIT CARD'
    CREDIT_CARD = 'CREDIT CARD'
    PAYMENT_TYPE_CHOICES = [
        (BANK_ACCOUNT, 'ACH'),
        (DEBIT_CARD, 'DEBIT CARD'),
        (CREDIT_CARD, 'CREDIT CARD')
    ]

    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    STATUS_CHOICES = [
        (PENDING, 'PENDING'),
        (PROCESSING, 'PROCESSING'),
        (COMPLETED, 'COMPLETED')
    ]

    id = models.AutoField(primary_key=True)
    amount_paid = models.FloatField(null=True, blank=True)
    date_paid = models.DateTimeField(null=True, blank=True, default=timezone.now)
    payment_type = models.CharField(max_length=12, choices=PAYMENT_TYPE_CHOICES, null=True, blank=True)
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, related_name='payments')
    tenant = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True)

    def __str__(self):
        return "$"+ str(self.amount_paid) + " on Invoice ID: " + str(self.invoice_id)


class BankAccounts(models.Model):
    BANK_ACCOUNT = 'ACH'
    DEBIT_CARD = 'DEBIT CARD'
    CREDIT_CARD = 'CREDIT CARD'
    ACCOUNT_TYPE_CHOICES = [
        (BANK_ACCOUNT, 'ACH'),
        (DEBIT_CARD, 'DEBIT CARD'),
        (CREDIT_CARD, 'CREDIT CARD')
    ]
    ACTIVE = 'ACTIVE'
    PAUSED = 'PAUSED'
    STATUS_CHOICES = [
        (ACTIVE, 'ACTIVE'),
        (PAUSED, 'PAUSED')
    ]

    id = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=255)
    account_type = models.CharField(
        max_length=12, choices=ACCOUNT_TYPE_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, null=True, blank=True)
    tenant = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='bankaccounts')

    def __str__(self):
        return str(self.id) + " - " + self.bank_name +" - " + str(self.tenant)


class ServiceRequests(models.Model):
    PLUMBING = 'PLUMBING'
    KITCHEN = 'KITCHEN'
    ELECTRICITY = 'ELECTRICITY'
    YARD = 'YARD'
    GARAGE = 'GARAGE'
    AIR_CONDITIONING = 'AIR CONDITIONING'
    OTHER = 'OTHER'
    CATEGORY_CHOICES = [
        (PLUMBING, 'PLUMBING'),
        (KITCHEN, 'KITCHEN'),
        (ELECTRICITY, 'ELECTRICITY'),
        (YARD, 'YARD'),
        (GARAGE, 'GARAGE'),
        (AIR_CONDITIONING, 'AIR CONDITIONING'),
        (OTHER, 'OTHER')
    ]
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETE = 'COMPLETE'
    STATUS_CHOICES = [
        (PENDING, 'PENDING'),
        (IN_PROGRESS, 'IN_PROGRESS'),
        (COMPLETE, 'COMPLETE')
    ]

    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    URGENT = 'URGENT'
    PRIORITY_CHOICES = [
        (LOW, 'LOW'),
        (MEDIUM, 'MEDIUM'),
        (HIGH, 'HIGH'),
        (URGENT, 'URGENT')
    ]

    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=16, choices=CATEGORY_CHOICES, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True, default=timezone.now)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES,
                              null=True, blank=True, default=PENDING)
    completed_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=11, choices=PRIORITY_CHOICES,
                              null=True, blank=True, default='low')
    tenant = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='servicerequests')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='servicerequests')

    def __str__(self):
        return str(self.id) + " - " + str(self.tenant)


