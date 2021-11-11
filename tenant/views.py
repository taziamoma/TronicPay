import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ScheduledPayments, Payments, BankAccounts, ServiceRequests
import users.models
from .forms import CreateServiceRequestForm


# Create your views here.

@login_required(login_url='login')
def DashboardView(request):
    title = "Dashboard"
    tenant = users.models.Tenant.objects.get(username=request.user.username)  # get the user tenant

    lease_start = tenant.lease_start
    lease_end = tenant.lease_end
    current_date = datetime.date.today()

    time_remaining = 0
    percentage = 0
    payment_history = 0

    context = {'title':title}
    if lease_start is not None or lease_end is not None:
        total_days = (lease_end - lease_start).days
        current_from_start = (current_date - lease_start).days
        time_remaining = total_days - current_from_start
        percentage = int((current_from_start / total_days) * 100)
        payment_history = Payments.objects.filter(tenant=tenant).order_by('-date_paid')
        context = {'title': title, 'lease_start': lease_start, 'lease_end': lease_end, 'percentage': percentage,
                   'time_remaining': time_remaining, 'payment_history': payment_history, 'tenant': tenant}

    return render(request, 'index.html', context)


@login_required(login_url='login')
def PaymentView(request):
    title = "Payment"
    context = {'title': title}
    return render(request, 'payment.html', context)


@login_required(login_url='login')
def AccountSummaryView(request):
    tenant = users.models.Tenant.objects.get(username=request.user.username)  # get the user tenant
    scheduled = ScheduledPayments.objects.filter(tenant=tenant, date_scheduled__isnull=False,
                                                 status="PENDING")  # get all scheduled payments that's date is not null
    bank_accounts = BankAccounts.objects.filter(tenant=tenant)  # get all back accounts for the associated user
    invoice = ScheduledPayments.objects.filter(tenant=tenant)  # return all invoices belonging to the tenant
    payment_history = Payments.objects.filter(tenant=tenant)
    pending = payment_history.filter(status="PENDING")
    title = "Account Summary"
    context = {'title': title, "scheduled": scheduled, 'bank_accounts': bank_accounts,
               "payment_history": payment_history, "pending": pending}
    return render(request, 'account-summary.html', context)


@login_required(login_url='login')
def ServiceRequestView(request):
    title = "Service Request"
    tenant = users.models.Tenant.objects.get(username=request.user.username)  # get the user tenant
    service_requests = ServiceRequests.objects.filter(tenant=tenant).order_by('-created')
    context = {'title': title, 'service_requests': service_requests}
    return render(request, 'service-request.html', context)


@login_required(login_url='login')
def CreateServiceRequestView(request):
    form = CreateServiceRequestForm()
    tenant = users.models.Tenant.objects.get(username=request.user.username)  # get the user tenant

    if request.method == "POST":
        form = CreateServiceRequestForm(request.POST)

        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.tenant = tenant
            service_request.unit = tenant.unit
            service_request.save()

            return redirect('service-request')

    context = {'form': form}
    return render(request, 'create-service-request.html', context)


@login_required(login_url='login')
def DeleteServiceRequestView(request, pk):
    ServiceRequests.objects.get(id=pk).delete()
    return redirect('service-request')


@login_required(login_url='login')
def RecurringPaymentView(request):
    title = "Recurring Payments"
    context = {'title': title}
    return render(request, 'recurring-payment.html', context)
