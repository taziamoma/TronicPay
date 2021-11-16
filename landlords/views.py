from django.shortcuts import render,  redirect
from django.contrib.auth.decorators import login_required
from .forms import CreateNewUnitForm, AddNewTenantForm, AddExistingTenantForm
from users.common import CustomUser, Tenancy, Unit
from users.decorators import landlord_required
from tenant.models import ServiceRequests

# Create your views here.
@login_required(login_url='login')
@landlord_required
def LandlordDashView(request):
    title = "Landlord Dashboard"
    context = {'title': title}
    return render(request, 'landlord.html', context)


@login_required(login_url='login')
@landlord_required
def UnitsView(request):
    title = "My Units"
    units = Unit.objects.filter(landlord=request.user)  # returns the units owned by the landlord

    context = {'title': title, 'units': units}
    return render(request, 'units.html', context)

@login_required(login_url='login')
@landlord_required
def UnitDetailView(request, pk):
    title = 'Unit'
    unit = Unit.objects.get(id=pk)
    service_requests = unit.getServiceRequests().order_by('-created')
    pending_service_requests = unit.getServiceRequests().filter(status="PENDING")
    in_progress_service_requests = unit.getServiceRequests().filter(status="IN_PROGRESS")
    completed_service_requests = unit.getServiceRequests().filter(status="COMPLETE")

    context = {'title':title, 'unit': unit, 'pending_service_requests': pending_service_requests, 'in_progress_service_requests':in_progress_service_requests, 'completed_service_requests': completed_service_requests, 'service_requests': service_requests }

    return render(request, 'view-unit.html', context)



@login_required(login_url='login')
@landlord_required
def MyTenantsView(request):
    title = "My Tenants"
    units = Unit.objects.filter(landlord=request.user)
    tenants = CustomUser.objects.filter(tenancies__landlord=request.user).distinct() #distinct prevents duplicate rows

    context = {'title': title}
    if tenants is not None:
        context = {'title': title, 'tenants': tenants}

    return render(request, 'my_tenants.html', context)

@login_required(login_url='login')
@landlord_required
def NewUnitView(request):
    title = "Add New Unit"
    landlord = request.user  # returns the landlord object of the user
    form = CreateNewUnitForm

    if request.method == 'POST':
        form = CreateNewUnitForm(request.POST)

        if form.is_valid():
            new_unit = form.save(commit=False)
            new_unit.landlord = landlord
            new_unit.save()

            return redirect('units')

    context = {'title': title, 'form':form}
    return render(request, 'new-unit.html', context)

@login_required(login_url='login')
@landlord_required
def DeleteUnitView(request, pk):
    Unit.objects.get(id=pk).delete()
    return redirect('units')

@login_required(login_url='login')
@landlord_required
def AddTenantToUnit(request, pk):
    title = "Add New Tenant"
    unit = Unit.objects.get(id=pk)
    new_tenant_form = AddNewTenantForm
    existing_tenant_form = AddExistingTenantForm(user=request.user)

    if request.method == 'POST':
        new_tenant_form = AddNewTenantForm(request.POST)
        existing_tenant_form = AddExistingTenantForm(request.POST, user=request.user)

        if new_tenant_form.is_valid():
            lease_start = new_tenant_form.cleaned_data['lease_start']
            lease_end = new_tenant_form.cleaned_data['lease_end']
            tenant = new_tenant_form.save()
            tenancy = Tenancy(unit=unit, tenant = tenant, lease_start=lease_start, lease_end=lease_end).save()

            unit.tenant = tenant
            unit.save()
            return redirect('units')

        elif existing_tenant_form.is_valid():
            tenant = existing_tenant_form.cleaned_data['tenant']
            lease_start = existing_tenant_form.cleaned_data['lease_start']
            lease_end = existing_tenant_form.cleaned_data['lease_end']
            tenancy = Tenancy(unit=unit, tenant = tenant, lease_start=lease_start, lease_end=lease_end).save()

            unit.tenant = tenant
            unit.save()
            return redirect('units')

    context = {'title': title, 'new_tenant_form': new_tenant_form, 'existing_tenant_form': existing_tenant_form}
    return render(request, 'add-tenant-to-unit.html', context)

@login_required(login_url='login')
@landlord_required
def ViewTenantView(request, pk):
    title = "View Tenant"
    tenant = CustomUser.objects.get(id=pk)
    tenancy = Tenancy.objects.filter(tenant=tenant)
    units = Unit.objects.filter(tenant=tenant)
    service_requests = ServiceRequests.objects.filter(tenant=tenant).order_by('-created')
    pending_service_requests = service_requests.filter(status="PENDING")
    in_progress_service_requests = service_requests.filter(status="IN_PROGRESS")
    completed_service_requests = service_requests.filter(status="COMPLETE")

    context = {'title': title, 'tenant': tenant, 'tenancy':tenancy, 'units': units, 'service_requests':service_requests, 'pending_service_requests': pending_service_requests, 'in_progress_service_requests':in_progress_service_requests,'completed_service_requests':completed_service_requests  }
    return render(request, 'view-tenant.html', context)