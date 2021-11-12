from django.utils import timezone
from django.conf import settings
from django.db import models
import users.models
import tenant.models

# Create your models here.

class Unit(models.Model):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    STATUS_CHOICES = [
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE')
    ]

    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=INACTIVE, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True, default=timezone.now)
    landlord = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='units')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    # def getOpenServiceRequests(self):
    #     pass

    def __str__(self):
        return str(self.address)