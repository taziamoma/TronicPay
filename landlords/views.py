from django.shortcuts import render,  redirect
from .models import Unit
from django.contrib.auth.decorators import login_required
from .forms import CreateNewUnitForm

# Create your views here.
@login_required(login_url='login')
def LandlordDashView(request):
    title = "Landlord Dashboard"
    context = {'title': title}
    return render(request, 'landlord.html', context)


@login_required(login_url='login')
def UnitsView(request):
    title = "My Units"
    landlord = Landlord.objects.get(user=request.user)  # returns the landlord object of the user
    units = Unit.objects.filter(landlord=landlord)  # returns the units owned by the landlord

    context = {'title': title, 'units': units}
    return render(request, 'units.html', context)


@login_required(login_url='login')
def MyTenantsView(request):
    title = "My Tenants"
    landlord = Landlord.objects.get(user=request.user)  # returns the landlord object of the user
    tenants = Tenant.objects.filter(landlord=landlord)

    context = {'title': title}
    if tenants is not None:
        context = {'title': title, 'tenants': tenants}

    return render(request, 'my_tenants.html', context)

@login_required(login_url='login')
def NewUnitView(request):
    title = "Add New Unit"
    landlord = Landlord.objects.get(user=request.user)  # returns the landlord object of the user
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

def DeleteUnitView(request, pk):
    Unit.objects.get(id=pk).delete()
    return redirect('units')