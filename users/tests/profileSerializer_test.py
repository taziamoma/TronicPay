from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from tronic_pay.serializers import ProfileSerializer

from tenant.tests.factories import (
    BankAccountsFactory,
    InvoiceFactory,
    ProfileFactory,
    ProfileWithForeignFactory,
    ServiceRequestsFactory,
)


class ProfileSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.profile = ProfileWithForeignFactory.create()

    def test_that_a_profile_is_correctly_serialized(self):
        profile = self.profile
        serializer = ProfileSerializer
        serialized_profile = serializer(profile).data

        assert serialized_profile['id'] == profile.id
        assert serialized_profile['name'] == profile.name
        assert serialized_profile['email'] == profile.email
        assert serialized_profile['username'] == profile.username
        assert serialized_profile['phone'] == profile.phone
        assert serialized_profile['created'] == profile.created
        assert serialized_profile['lease_start'] == profile.lease_start
        assert serialized_profile['lease_end'] == profile.lease_end
        assert serialized_profile['address'] == profile.address
        assert serialized_profile['zipcode'] == profile.zipcode

        assert len(serialized_profile['invoices']) == profile.invoices.count()

        assert len(serialized_profile['bankaccountss']) == profile.bankaccountss.count()

        assert len(serialized_profile['servicerequestss']) == profile.servicerequestss.count()
