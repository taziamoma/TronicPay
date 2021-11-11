from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Tenant
from django.contrib.auth.models import User


# @receiver(post_save, sender=Tenant)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Tenant.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
        )


# @receiver(post_delete, sender=Tenant)
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, sender=Tenant)