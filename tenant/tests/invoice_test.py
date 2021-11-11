import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Invoice
from .factories import InvoiceFactory, ProfileFactory

faker = Factory.create()


class Invoice_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        InvoiceFactory.create_batch(size=3)
        self.profile = ProfileFactory.create()

    def test_create_invoice(self):
        """
        Ensure we can create a new invoice object.
        """
        client = self.api_client
        invoice_count = Invoice.objects.count()
        invoice_dict = factory.build(dict, FACTORY_CLASS=InvoiceFactory, profile=self.profile.id)
        response = client.post(reverse('invoice-list'), invoice_dict)
        created_invoice_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Invoice.objects.count() == invoice_count + 1
        invoice = Invoice.objects.get(pk=created_invoice_pk)

        assert invoice_dict['type'] == invoice.type
        assert invoice_dict['amount_total'] == invoice.amount_total
        assert invoice_dict['amount_paid'] == invoice.amount_paid
        assert invoice_dict['due_date'] == invoice.due_date.isoformat()
        assert invoice_dict['date_paid'] == invoice.date_paid.isoformat()
        assert invoice_dict['created'] == invoice.created.isoformat()
        assert invoice_dict['status'] == invoice.status
        assert invoice_dict['scheduled_pay_date'] == invoice.scheduled_pay_date.isoformat()

    def test_get_one(self):
        client = self.api_client
        invoice_pk = Invoice.objects.first().pk
        invoice_detail_url = reverse('invoice-detail', kwargs={'pk': invoice_pk})
        response = client.get(invoice_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('invoice-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Invoice.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        invoice_qs = Invoice.objects.all()
        invoice_count = Invoice.objects.count()

        for i, invoice in enumerate(invoice_qs, start=1):
            response = client.delete(reverse('invoice-detail', kwargs={'pk': invoice.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert invoice_count - i == Invoice.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        invoice_pk = Invoice.objects.first().pk
        invoice_detail_url = reverse('invoice-detail', kwargs={'pk': invoice_pk})
        invoice_dict = factory.build(dict, FACTORY_CLASS=InvoiceFactory, profile=self.profile.id)
        response = client.patch(invoice_detail_url, data=invoice_dict)
        assert response.status_code == status.HTTP_200_OK

        assert invoice_dict['type'] == response.data['type']
        assert invoice_dict['amount_total'] == response.data['amount_total']
        assert invoice_dict['amount_paid'] == response.data['amount_paid']
        assert invoice_dict['due_date'] == response.data['due_date'].replace('Z', '+00:00')
        assert invoice_dict['date_paid'] == response.data['date_paid'].replace('Z', '+00:00')
        assert invoice_dict['created'] == response.data['created'].replace('Z', '+00:00')
        assert invoice_dict['status'] == response.data['status']
        assert invoice_dict['scheduled_pay_date'] == response.data['scheduled_pay_date'].replace(
            'Z', '+00:00')

    def test_update_amount_total_with_incorrect_value_data_type(self):
        client = self.api_client
        invoice = Invoice.objects.first()
        invoice_detail_url = reverse('invoice-detail', kwargs={'pk': invoice.pk})
        invoice_amount_total = invoice.amount_total
        data = {
            'amount_total': faker.pystr(),
        }
        response = client.patch(invoice_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert invoice_amount_total == Invoice.objects.first().amount_total

    def test_update_amount_paid_with_incorrect_value_data_type(self):
        client = self.api_client
        invoice = Invoice.objects.first()
        invoice_detail_url = reverse('invoice-detail', kwargs={'pk': invoice.pk})
        invoice_amount_paid = invoice.amount_paid
        data = {
            'amount_paid': faker.pystr(),
        }
        response = client.patch(invoice_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert invoice_amount_paid == Invoice.objects.first().amount_paid

    def test_update_due_date_with_incorrect_value_data_type(self):
        client = self.api_client
        invoice = Invoice.objects.first()
        invoice_detail_url = reverse('invoice-detail', kwargs={'pk': invoice.pk})
        invoice_due_date = invoice.due_date
        data = {
            'due_date': faker.pystr(),
        }
        response = client.patch(invoice_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert invoice_due_date == Invoice.objects.first().due_date

    def test_update_date_paid_with_incorrect_value_data_type(self):
        client = self.api_client
        invoice = Invoice.objects.first()
        invoice_detail_url = reverse('invoice-detail', kwargs={'pk': invoice.pk})
        invoice_date_paid = invoice.date_paid
        data = {
            'date_paid': faker.pystr(),
        }
        response = client.patch(invoice_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert invoice_date_paid == Invoice.objects.first().date_paid

    def test_update_created_with_incorrect_value_data_type(self):
        client = self.api_client
        invoice = Invoice.objects.first()
        invoice_detail_url = reverse('invoice-detail', kwargs={'pk': invoice.pk})
        invoice_created = invoice.created
        data = {
            'created': faker.pystr(),
        }
        response = client.patch(invoice_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert invoice_created == Invoice.objects.first().created

    def test_update_scheduled_pay_date_with_incorrect_value_data_type(self):
        client = self.api_client
        invoice = Invoice.objects.first()
        invoice_detail_url = reverse('invoice-detail', kwargs={'pk': invoice.pk})
        invoice_scheduled_pay_date = invoice.scheduled_pay_date
        data = {
            'scheduled_pay_date': faker.pystr(),
        }
        response = client.patch(invoice_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert invoice_scheduled_pay_date == Invoice.objects.first().scheduled_pay_date

    def test_update_type_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        invoice = Invoice.objects.first()
        invoice_detail_url = reverse('invoice-detail', kwargs={'pk': invoice.pk})
        invoice_type = invoice.type
        data = {
            'type': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(invoice_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert invoice_type == Invoice.objects.first().type

    def test_update_status_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        invoice = Invoice.objects.first()
        invoice_detail_url = reverse('invoice-detail', kwargs={'pk': invoice.pk})
        invoice_status = invoice.status
        data = {
            'status': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(invoice_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert invoice_status == Invoice.objects.first().status
