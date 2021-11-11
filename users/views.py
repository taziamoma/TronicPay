from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import EditProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def loginUser(request):
    title = "Login"

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        if user is not None:
            login(request, user)

            return redirect('dashboard')
        else:
            messages.error(request, 'Username or password is incorrect')


    context = {'title':title}
    return render(request, 'users/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def EditProfileView(request):
    tenant = Tenant.objects.get(username=request.user.username) #get user tenant information
    form = EditProfileForm(instance=tenant) #get the instance of the user tenant

    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('edit-tenant')

    context = {'form': form}
    return render(request, 'users/edit-profile.html', context)