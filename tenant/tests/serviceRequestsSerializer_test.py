from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from tronic_pay.serializers import ServiceRequestsSerializer

from .factories import ServiceRequestsFactory


class ServiceRequestsSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.serviceRequests = ServiceRequestsFactory.create()

    def test_that_a_serviceRequests_is_correctly_serialized(self):
        serviceRequests = self.serviceRequests
        serializer = ServiceRequestsSerializer
        serialized_serviceRequests = serializer(serviceRequests).data

        assert serialized_serviceRequests['id'] == serviceRequests.id
        assert serialized_serviceRequests['category'] == serviceRequests.category
        assert serialized_serviceRequests['created'] == serviceRequests.created
        assert serialized_serviceRequests['description'] == serviceRequests.description
        assert serialized_serviceRequests['status'] == serviceRequests.status
        assert serialized_serviceRequests['completed_date'] == serviceRequests.completed_date
