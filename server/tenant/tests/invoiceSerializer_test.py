from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from tronic_pay.serializers import InvoiceSerializer

from .factories import InvoiceFactory


class InvoiceSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.invoice = InvoiceFactory.create()

    def test_that_a_invoice_is_correctly_serialized(self):
        invoice = self.invoice
        serializer = InvoiceSerializer
        serialized_invoice = serializer(invoice).data

        assert serialized_invoice['id'] == invoice.id
        assert serialized_invoice['type'] == invoice.type
        assert serialized_invoice['amount_total'] == invoice.amount_total
        assert serialized_invoice['amount_paid'] == invoice.amount_paid
        assert serialized_invoice['due_date'] == invoice.due_date
        assert serialized_invoice['date_paid'] == invoice.date_paid
        assert serialized_invoice['created'] == invoice.created
        assert serialized_invoice['status'] == invoice.status
        assert serialized_invoice['scheduled_pay_date'] == invoice.scheduled_pay_date
