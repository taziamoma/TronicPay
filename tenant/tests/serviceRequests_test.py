import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import ServiceRequests
from .factories import ProfileFactory, ServiceRequestsFactory

faker = Factory.create()


class ServiceRequests_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        ServiceRequestsFactory.create_batch(size=3)
        self.profile = ProfileFactory.create()

    def test_create_serviceRequests(self):
        """
        Ensure we can create a new serviceRequests object.
        """
        client = self.api_client
        serviceRequests_count = ServiceRequests.objects.count()
        serviceRequests_dict = factory.build(
            dict, FACTORY_CLASS=ServiceRequestsFactory, profile=self.profile.id)
        response = client.post(reverse('serviceRequests-list'), serviceRequests_dict)
        created_serviceRequests_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert ServiceRequests.objects.count() == serviceRequests_count + 1
        serviceRequests = ServiceRequests.objects.get(pk=created_serviceRequests_pk)

        assert serviceRequests_dict['category'] == serviceRequests.category
        assert serviceRequests_dict['created'] == serviceRequests.created.isoformat()
        assert serviceRequests_dict['description'] == serviceRequests.description
        assert serviceRequests_dict['status'] == serviceRequests.status
        assert serviceRequests_dict['completed_date'] == serviceRequests.completed_date.isoformat()

    def test_get_one(self):
        client = self.api_client
        serviceRequests_pk = ServiceRequests.objects.first().pk
        serviceRequests_detail_url = reverse(
            'serviceRequests-detail', kwargs={'pk': serviceRequests_pk})
        response = client.get(serviceRequests_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('serviceRequests-list'))
        assert response.status_code == status.HTTP_200_OK
        assert ServiceRequests.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        serviceRequests_qs = ServiceRequests.objects.all()
        serviceRequests_count = ServiceRequests.objects.count()

        for i, serviceRequests in enumerate(serviceRequests_qs, start=1):
            response = client.delete(reverse('serviceRequests-detail',
                                     kwargs={'pk': serviceRequests.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert serviceRequests_count - i == ServiceRequests.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        serviceRequests_pk = ServiceRequests.objects.first().pk
        serviceRequests_detail_url = reverse(
            'serviceRequests-detail', kwargs={'pk': serviceRequests_pk})
        serviceRequests_dict = factory.build(
            dict, FACTORY_CLASS=ServiceRequestsFactory, profile=self.profile.id)
        response = client.patch(serviceRequests_detail_url, data=serviceRequests_dict)
        assert response.status_code == status.HTTP_200_OK

        assert serviceRequests_dict['category'] == response.data['category']
        assert serviceRequests_dict['created'] == response.data['created'].replace('Z', '+00:00')
        assert serviceRequests_dict['description'] == response.data['description']
        assert serviceRequests_dict['status'] == response.data['status']
        assert serviceRequests_dict['completed_date'] == response.data['completed_date'].replace(
            'Z', '+00:00')

    def test_update_created_with_incorrect_value_data_type(self):
        client = self.api_client
        serviceRequests = ServiceRequests.objects.first()
        serviceRequests_detail_url = reverse(
            'serviceRequests-detail', kwargs={'pk': serviceRequests.pk})
        serviceRequests_created = serviceRequests.created
        data = {
            'created': faker.pystr(),
        }
        response = client.patch(serviceRequests_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert serviceRequests_created == ServiceRequests.objects.first().created

    def test_update_completed_date_with_incorrect_value_data_type(self):
        client = self.api_client
        serviceRequests = ServiceRequests.objects.first()
        serviceRequests_detail_url = reverse(
            'serviceRequests-detail', kwargs={'pk': serviceRequests.pk})
        serviceRequests_completed_date = serviceRequests.completed_date
        data = {
            'completed_date': faker.pystr(),
        }
        response = client.patch(serviceRequests_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert serviceRequests_completed_date == ServiceRequests.objects.first().completed_date

    def test_update_category_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        serviceRequests = ServiceRequests.objects.first()
        serviceRequests_detail_url = reverse(
            'serviceRequests-detail', kwargs={'pk': serviceRequests.pk})
        serviceRequests_category = serviceRequests.category
        data = {
            'category': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(serviceRequests_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert serviceRequests_category == ServiceRequests.objects.first().category

    def test_update_description_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        serviceRequests = ServiceRequests.objects.first()
        serviceRequests_detail_url = reverse(
            'serviceRequests-detail', kwargs={'pk': serviceRequests.pk})
        serviceRequests_description = serviceRequests.description
        data = {
            'description': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(serviceRequests_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert serviceRequests_description == ServiceRequests.objects.first().description

    def test_update_status_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        serviceRequests = ServiceRequests.objects.first()
        serviceRequests_detail_url = reverse(
            'serviceRequests-detail', kwargs={'pk': serviceRequests.pk})
        serviceRequests_status = serviceRequests.status
        data = {
            'status': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(serviceRequests_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert serviceRequests_status == ServiceRequests.objects.first().status
