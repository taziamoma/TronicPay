from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import datetime
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # custom fields
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zipcode = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.email

    def is_landlord(self):
        return self.assets.exists()

    def is_tenant(self):
        return self.tenancies.exists()


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
    landlord = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assets')
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tenancies', null=True,
                               blank=True)

    def getOpenServiceRequests(self):
        from tenant.models import ServiceRequests
        service_requests = ServiceRequests.objects.filter(unit=self).exclude(status="COMPLETE")
        return service_requests

    def getServiceRequests(self):
        from tenant.models import ServiceRequests
        service_requests = ServiceRequests.objects.filter(unit=self)
        return service_requests

    def getLeasePercentage(self):
        tenancy = Tenancy.objects.get(unit=self)
        return tenancy.getLeasePercentage()

    def getLeaseStart(self):
        tenancy = Tenancy.objects.get(unit=self)
        return tenancy.lease_start

    def getLeaseEnd(self):
        tenancy = Tenancy.objects.get(unit=self)
        return tenancy.lease_end

    def __str__(self):
        return str(self.address)


class Tenancy(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    tenant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(null=True, blank=True, default=timezone.now)
    lease_start = models.DateField(null=True, blank=True)
    lease_end = models.DateField(null=True, blank=True)

    def updateUnit(self):
        unit = self.unit
        unit.tenant = self.tenant
        unit.save()

    def getTimeRemaining(self):
        current_date = datetime.date.today()
        total_days = (self.lease_end - self.lease_start).days
        current_from_start = (current_date - self.lease_start).days
        time_remaining = total_days - current_from_start
        return time_remaining

    def getLeasePercentage(self):
        current_date = datetime.date.today()
        total_days = (self.lease_end - self.lease_start).days
        current_from_start = (current_date - self.lease_start).days
        percentage = int((current_from_start) / (total_days) * 100)
        return percentage

    def __str__(self):
        return str(self.tenant.first_name) + " " + str(self.tenant.last_name) + " - " + str(self.unit.address)
