from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from tronic_pay.serializers import BankAccountsSerializer

from .factories import BankAccountsFactory


class BankAccountsSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.bankAccounts = BankAccountsFactory.create()

    def test_that_a_bankAccounts_is_correctly_serialized(self):
        bankAccounts = self.bankAccounts
        serializer = BankAccountsSerializer
        serialized_bankAccounts = serializer(bankAccounts).data

        assert serialized_bankAccounts['id'] == bankAccounts.id
        assert serialized_bankAccounts['bank_name'] == bankAccounts.bank_name
        assert serialized_bankAccounts['account_type'] == bankAccounts.account_type
        assert serialized_bankAccounts['status'] == bankAccounts.status
