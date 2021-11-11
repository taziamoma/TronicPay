import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from tenant.models import Tenant
from tenant.tests.factories import (
    BankAccountsFactory,
    InvoiceFactory,
    ProfileFactory,
    ServiceRequestsFactory,
)

faker = Factory.create()


class Profile_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        ProfileFactory.create_batch(size=3)

    def test_create_profile(self):
        """
        Ensure we can create a new tenant object.
        """
        client = self.api_client
        profile_count = Tenant.objects.count()
        profile_dict = factory.build(dict, FACTORY_CLASS=ProfileFactory)
        response = client.post(reverse('tenant-list'), profile_dict)
        created_profile_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Tenant.objects.count() == profile_count + 1
        profile = Tenant.objects.get(pk=created_profile_pk)

        assert profile_dict['name'] == profile.name
        assert profile_dict['email'] == profile.email
        assert profile_dict['username'] == profile.username
        assert profile_dict['phone'] == profile.phone
        assert profile_dict['created'] == profile.created.isoformat()
        assert profile_dict['lease_start'] == profile.lease_start.isoformat()
        assert profile_dict['lease_end'] == profile.lease_end.isoformat()
        assert profile_dict['address'] == profile.address
        assert profile_dict['zipcode'] == profile.zipcode

    def test_get_one(self):
        client = self.api_client
        profile_pk = Tenant.objects.first().pk
        profile_detail_url = reverse('tenant-detail', kwargs={'pk': profile_pk})
        response = client.get(profile_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('tenant-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Tenant.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        profile_qs = Tenant.objects.all()
        profile_count = Tenant.objects.count()

        for i, profile in enumerate(profile_qs, start=1):
            response = client.delete(reverse('tenant-detail', kwargs={'pk': profile.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert profile_count - i == Tenant.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        profile_pk = Tenant.objects.first().pk
        profile_detail_url = reverse('tenant-detail', kwargs={'pk': profile_pk})
        profile_dict = factory.build(dict, FACTORY_CLASS=ProfileFactory)
        response = client.patch(profile_detail_url, data=profile_dict)
        assert response.status_code == status.HTTP_200_OK

        assert profile_dict['name'] == response.data['name']
        assert profile_dict['email'] == response.data['email']
        assert profile_dict['username'] == response.data['username']
        assert profile_dict['phone'] == response.data['phone']
        assert profile_dict['created'] == response.data['created'].replace('Z', '+00:00')
        assert profile_dict['lease_start'] == response.data['lease_start'].replace('Z', '+00:00')
        assert profile_dict['lease_end'] == response.data['lease_end'].replace('Z', '+00:00')
        assert profile_dict['address'] == response.data['address']
        assert profile_dict['zipcode'] == response.data['zipcode']

    def test_update_created_with_incorrect_value_data_type(self):
        client = self.api_client
        profile = Tenant.objects.first()
        profile_detail_url = reverse('tenant-detail', kwargs={'pk': profile.pk})
        profile_created = profile.created
        data = {
            'created': faker.pystr(),
        }
        response = client.patch(profile_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert profile_created == Tenant.objects.first().created

    def test_update_lease_start_with_incorrect_value_data_type(self):
        client = self.api_client
        profile = Tenant.objects.first()
        profile_detail_url = reverse('tenant-detail', kwargs={'pk': profile.pk})
        profile_lease_start = profile.lease_start
        data = {
            'lease_start': faker.pystr(),
        }
        response = client.patch(profile_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert profile_lease_start == Tenant.objects.first().lease_start

    def test_update_lease_end_with_incorrect_value_data_type(self):
        client = self.api_client
        profile = Tenant.objects.first()
        profile_detail_url = reverse('tenant-detail', kwargs={'pk': profile.pk})
        profile_lease_end = profile.lease_end
        data = {
            'lease_end': faker.pystr(),
        }
        response = client.patch(profile_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert profile_lease_end == Tenant.objects.first().lease_end

    def test_update_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        profile = Tenant.objects.first()
        profile_detail_url = reverse('tenant-detail', kwargs={'pk': profile.pk})
        profile_name = profile.name
        data = {
            'name': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(profile_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert profile_name == Tenant.objects.first().name

    def test_update_email_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        profile = Tenant.objects.first()
        profile_detail_url = reverse('tenant-detail', kwargs={'pk': profile.pk})
        profile_email = profile.email
        data = {
            'email': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(profile_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert profile_email == Tenant.objects.first().email

    def test_update_username_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        profile = Tenant.objects.first()
        profile_detail_url = reverse('tenant-detail', kwargs={'pk': profile.pk})
        profile_username = profile.username
        data = {
            'username': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(profile_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert profile_username == Tenant.objects.first().username

    def test_update_phone_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        profile = Tenant.objects.first()
        profile_detail_url = reverse('tenant-detail', kwargs={'pk': profile.pk})
        profile_phone = profile.phone
        data = {
            'phone': faker.pystr(min_chars=12, max_chars=12),
        }
        response = client.patch(profile_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert profile_phone == Tenant.objects.first().phone

    def test_update_address_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        profile = Tenant.objects.first()
        profile_detail_url = reverse('tenant-detail', kwargs={'pk': profile.pk})
        profile_address = profile.address
        data = {
            'address': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(profile_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert profile_address == Tenant.objects.first().address

    def test_update_zipcode_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        profile = Tenant.objects.first()
        profile_detail_url = reverse('tenant-detail', kwargs={'pk': profile.pk})
        profile_zipcode = profile.zipcode
        data = {
            'zipcode': faker.pystr(min_chars=7, max_chars=7),
        }
        response = client.patch(profile_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert profile_zipcode == Tenant.objects.first().zipcode
