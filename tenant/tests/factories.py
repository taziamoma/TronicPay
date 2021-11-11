from datetime import timedelta, timezone
from random import randint, uniform

import factory
from factory import LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory

from tronic_pay.models import BankAccounts, Invoice, Profile, ServiceRequests

faker = Factory.create()


class InvoiceFactory(DjangoModelFactory):
    class Meta:
        model = Invoice

    profile = factory.SubFactory('tronic_pay.tests.factories.ProfileFactory')
    type = fuzzy.FuzzyChoice(Invoice.TYPE_CHOICES, getter=lambda c: c[0])
    amount_total = LazyAttribute(lambda o: uniform(0, 10000))
    amount_paid = LazyAttribute(lambda o: uniform(0, 10000))
    due_date = LazyAttribute(lambda o: faker.date_time(tzinfo=timezone(timedelta(0))).isoformat())
    date_paid = LazyAttribute(lambda o: faker.date_time(tzinfo=timezone(timedelta(0))).isoformat())
    created = LazyAttribute(lambda o: faker.date_time(tzinfo=timezone(timedelta(0))).isoformat())
    status = fuzzy.FuzzyChoice(Invoice.STATUS_CHOICES, getter=lambda c: c[0])
    scheduled_pay_date = LazyAttribute(lambda o: faker.date_time(
        tzinfo=timezone(timedelta(0))).isoformat())


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    email = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    username = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    phone = LazyAttribute(lambda o: faker.text(max_nb_chars=11))
    created = LazyAttribute(lambda o: faker.date_time(tzinfo=timezone(timedelta(0))).isoformat())
    lease_start = LazyAttribute(lambda o: faker.date_time(
        tzinfo=timezone(timedelta(0))).isoformat())
    lease_end = LazyAttribute(lambda o: faker.date_time(tzinfo=timezone(timedelta(0))).isoformat())
    address = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    zipcode = LazyAttribute(lambda o: faker.text(max_nb_chars=6))


class ProfileWithForeignFactory(ProfileFactory):
    @factory.post_generation
    def invoices(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                InvoiceFactory(profile=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                InvoiceFactory(profile=obj)

    @factory.post_generation
    def bankaccountss(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                BankAccountsFactory(profile=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                BankAccountsFactory(profile=obj)

    @factory.post_generation
    def servicerequestss(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                ServiceRequestsFactory(profile=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                ServiceRequestsFactory(profile=obj)


class BankAccountsFactory(DjangoModelFactory):
    class Meta:
        model = BankAccounts

    profile = factory.SubFactory('tronic_pay.tests.factories.ProfileFactory')
    bank_name = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    account_type = fuzzy.FuzzyChoice(BankAccounts.ACCOUNT_TYPE_CHOICES, getter=lambda c: c[0])
    status = fuzzy.FuzzyChoice(BankAccounts.STATUS_CHOICES, getter=lambda c: c[0])


class ServiceRequestsFactory(DjangoModelFactory):
    class Meta:
        model = ServiceRequests

    profile = factory.SubFactory('tronic_pay.tests.factories.ProfileFactory')
    category = fuzzy.FuzzyChoice(ServiceRequests.CATEGORY_CHOICES, getter=lambda c: c[0])
    created = LazyAttribute(lambda o: faker.date_time(tzinfo=timezone(timedelta(0))).isoformat())
    description = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    status = fuzzy.FuzzyChoice(ServiceRequests.STATUS_CHOICES, getter=lambda c: c[0])
    completed_date = LazyAttribute(lambda o: faker.date_time(
        tzinfo=timezone(timedelta(0))).isoformat())
