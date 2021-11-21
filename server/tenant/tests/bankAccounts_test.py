import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import BankAccounts
from .factories import BankAccountsFactory, ProfileFactory

faker = Factory.create()


class BankAccounts_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        BankAccountsFactory.create_batch(size=3)
        self.profile = ProfileFactory.create()

    def test_create_bankAccounts(self):
        """
        Ensure we can create a new bankAccounts object.
        """
        client = self.api_client
        bankAccounts_count = BankAccounts.objects.count()
        bankAccounts_dict = factory.build(
            dict, FACTORY_CLASS=BankAccountsFactory, profile=self.profile.id)
        response = client.post(reverse('bankAccounts-list'), bankAccounts_dict)
        created_bankAccounts_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert BankAccounts.objects.count() == bankAccounts_count + 1
        bankAccounts = BankAccounts.objects.get(pk=created_bankAccounts_pk)

        assert bankAccounts_dict['bank_name'] == bankAccounts.bank_name
        assert bankAccounts_dict['account_type'] == bankAccounts.account_type
        assert bankAccounts_dict['status'] == bankAccounts.status

    def test_get_one(self):
        client = self.api_client
        bankAccounts_pk = BankAccounts.objects.first().pk
        bankAccounts_detail_url = reverse('bankAccounts-detail', kwargs={'pk': bankAccounts_pk})
        response = client.get(bankAccounts_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('bankAccounts-list'))
        assert response.status_code == status.HTTP_200_OK
        assert BankAccounts.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        bankAccounts_qs = BankAccounts.objects.all()
        bankAccounts_count = BankAccounts.objects.count()

        for i, bankAccounts in enumerate(bankAccounts_qs, start=1):
            response = client.delete(reverse('bankAccounts-detail', kwargs={'pk': bankAccounts.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert bankAccounts_count - i == BankAccounts.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        bankAccounts_pk = BankAccounts.objects.first().pk
        bankAccounts_detail_url = reverse('bankAccounts-detail', kwargs={'pk': bankAccounts_pk})
        bankAccounts_dict = factory.build(
            dict, FACTORY_CLASS=BankAccountsFactory, profile=self.profile.id)
        response = client.patch(bankAccounts_detail_url, data=bankAccounts_dict)
        assert response.status_code == status.HTTP_200_OK

        assert bankAccounts_dict['bank_name'] == response.data['bank_name']
        assert bankAccounts_dict['account_type'] == response.data['account_type']
        assert bankAccounts_dict['status'] == response.data['status']

    def test_update_bank_name_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        bankAccounts = BankAccounts.objects.first()
        bankAccounts_detail_url = reverse('bankAccounts-detail', kwargs={'pk': bankAccounts.pk})
        bankAccounts_bank_name = bankAccounts.bank_name
        data = {
            'bank_name': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(bankAccounts_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert bankAccounts_bank_name == BankAccounts.objects.first().bank_name

    def test_update_account_type_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        bankAccounts = BankAccounts.objects.first()
        bankAccounts_detail_url = reverse('bankAccounts-detail', kwargs={'pk': bankAccounts.pk})
        bankAccounts_account_type = bankAccounts.account_type
        data = {
            'account_type': faker.pystr(min_chars=21, max_chars=21),
        }
        response = client.patch(bankAccounts_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert bankAccounts_account_type == BankAccounts.objects.first().account_type

    def test_update_status_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        bankAccounts = BankAccounts.objects.first()
        bankAccounts_detail_url = reverse('bankAccounts-detail', kwargs={'pk': bankAccounts.pk})
        bankAccounts_status = bankAccounts.status
        data = {
            'status': faker.pystr(min_chars=7, max_chars=7),
        }
        response = client.patch(bankAccounts_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert bankAccounts_status == BankAccounts.objects.first().status
