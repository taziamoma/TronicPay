import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ScheduledPayments, Payments, BankAccounts, ServiceRequests
from users.models import CustomUser, Tenancy
from landlords.models import Unit
from .forms import CreateServiceRequestForm


# Create your views here.

@login_required(login_url='login')
def DashboardView(request):
    title = "Dashboard"
    profile = CustomUser.objects.get(email=request.user.email)  # get the user tenant

    lease_start = Tenancy.objects.get(tenant=profile).lease_start
    lease_end = Tenancy.objects.get(tenant=profile).lease_end
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
        payment_history = Payments.objects.filter(tenant=profile).order_by('-date_paid')
        context = {'title': title, 'lease_start': lease_start, 'lease_end': lease_end, 'percentage': percentage,
                   'time_remaining': time_remaining, 'payment_history': payment_history, 'profile': profile}

    return render(request, 'index.html', context)


@login_required(login_url='login')
def PaymentView(request):
    title = "Payment"
    context = {'title': title}
    return render(request, 'payment.html', context)


@login_required(login_url='login')
def AccountSummaryView(request):
    profile = CustomUser.objects.get(email=request.user.email)  # get the user profile
    scheduled = ScheduledPayments.objects.filter(tenant=profile, date_scheduled__isnull=False,
                                                 status="PENDING")  # get all scheduled payments that's date is not null
    bank_accounts = BankAccounts.objects.filter(tenant=profile)  # get all back accounts for the associated user
    invoice = ScheduledPayments.objects.filter(tenant=profile)  # return all invoices belonging to the profile
    payment_history = Payments.objects.filter(tenant=profile)
    pending = payment_history.filter(status="PENDING")
    title = "Account Summary"
    context = {'title': title, "scheduled": scheduled, 'bank_accounts': bank_accounts,
               "payment_history": payment_history, "pending": pending}
    return render(request, 'account-summary.html', context)


@login_required(login_url='login')
def ServiceRequestView(request):
    title = "Service Request"
    profile = CustomUser.objects.get(email=request.user.email)  # get the user profile
    service_requests = ServiceRequests.objects.filter(tenant=profile).order_by('-created')
    context = {'title': title, 'service_requests': service_requests}
    return render(request, 'service-request.html', context)


@login_required(login_url='login')
def CreateServiceRequestView(request):
    form = CreateServiceRequestForm()
    profile = CustomUser.objects.get(email=request.user.email)  # get the user profile

    if request.method == "POST":
        form = CreateServiceRequestForm(request.POST)

        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.tenant = profile
            service_request.unit = Unit.objects.get(tenant=profile)
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
