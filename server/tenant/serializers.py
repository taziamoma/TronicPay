from rest_framework import serializers

from .models import BankAccounts, Invoice, Tenant, ServiceRequests


class InvoiceSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(
        queryset=Tenant.objects.all(),
    )

    class Meta:
        model = Invoice
        fields = ['id', 'type', 'amount_total', 'amount_paid', 'due_date',
                  'date_paid', 'created', 'status', 'scheduled_pay_date', 'tenant']


class ProfileSerializer(serializers.ModelSerializer):
    invoices = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Invoice.objects.all(),
        required=False
    )
    bankaccountss = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=BankAccounts.objects.all(),
        required=False
    )
    servicerequestss = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=ServiceRequests.objects.all(),
        required=False
    )

    class Meta:
        model = Tenant
        fields = ['id', 'name', 'email', 'username', 'phone', 'created', 'lease_start',
                  'lease_end', 'address', 'zipcode', 'invoices', 'bankaccountss', 'servicerequestss']


class BankAccountsSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(
        queryset=Tenant.objects.all(),
    )

    class Meta:
        model = BankAccounts
        fields = ['id', 'bank_name', 'account_type', 'status', 'tenant']


class ServiceRequestsSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(
        queryset=Tenant.objects.all(),
    )

    class Meta:
        model = ServiceRequests
        fields = ['id', 'category', 'created', 'description', 'status', 'completed_date', 'tenant']
