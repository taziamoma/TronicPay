from django.forms import ModelForm
from django import forms
from users.common import Unit, CustomUser, Tenancy
from django.contrib.auth.forms import UserCreationForm


class CreateNewUnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = ['address', 'state', 'city', 'zipcode']

    def __init__(self, *args, **kwargs):
        super(CreateNewUnitForm, self).__init__(*args, **kwargs)

        self.fields['address'].widget.attrs.update({'class': 'form-control', 'name': 'address', 'required': 'required'})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'name': 'state', 'required': 'required'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'name': 'city', 'required': 'required'})
        self.fields['zipcode'].widget.attrs.update({'class': 'form-control', 'name': 'zipcode', 'required': 'required'})


class CreateNewTenantForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'address', 'city', 'state',
                  'zipcode']

    def __init__(self, *args, **kwargs):
        super(CreateNewTenantForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'name': 'email', 'required': 'required'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'name': 'password1', 'required': 'required'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'name': 'password2', 'required': 'required'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'name': 'first_name', 'required': 'required'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'name': 'last_name', 'required': 'required'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'name': 'phone'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'name': 'address'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'name': 'city'})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'name': 'state'})
        self.fields['zipcode'].widget.attrs.update({'class': 'form-control', 'name': 'zipcode'})


class AddNewTenantForm(UserCreationForm):
    lease_start = forms.DateField()
    lease_end = forms.DateField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'address', 'city', 'state',
                  'zipcode', 'lease_start', 'lease_end']

    def __init__(self, *args, **kwargs):
        super(AddNewTenantForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'name': name, 'required': 'required'})

        self.fields['address'].widget.attrs.update({'class': 'form-control', 'name': 'address'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'name': 'city'})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'name': 'state'})
        self.fields['zipcode'].widget.attrs.update({'class': 'form-control', 'name': 'zipcode'})
        self.fields['lease_start'].widget.attrs.update(
            {'class': 'datepicker-here form-control digits', 'name': 'lease_start', 'data-language': 'en'})
        self.fields['lease_end'].widget.attrs.update(
            {'class': 'datepicker-here form-control digits', 'name': 'lease_end', 'data-language': 'en'})


class AddExistingTenantForm(ModelForm):
    user = None

    class Meta:
        model = Tenancy
        fields = ['tenant', 'lease_start', 'lease_end']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AddExistingTenantForm, self).__init__(*args, **kwargs)
        tenants = CustomUser.objects.filter(
            tenancies__landlord=user).distinct()  # Queries the data base for users who have the request.user as landlord

        self.fields['tenant'].queryset = tenants
        # self.fields['tenant'].widget.attrs.update({'class': 'form-control', 'name': 'address'})
        self.fields['lease_start'].widget.attrs.update(
            {'class': 'datepicker-here form-control digits', 'name': 'lease_start', 'data-language': 'en'})
        self.fields['lease_end'].widget.attrs.update(
            {'class': 'datepicker-here form-control digits', 'name': 'lease_end', 'data-language': 'en'})
