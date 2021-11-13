from django.forms import ModelForm
from django import forms
from users.common import Unit, CustomUser
from django.contrib.auth.forms import UserCreationForm

class CreateNewUnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = ['address', 'state', 'city', 'zipcode']


    def __init__(self, *args, **kwargs):
        super(CreateNewUnitForm, self).__init__(*args, **kwargs)

        self.fields['address'].widget.attrs.update({'class':'form-control', 'name': 'address', 'required': 'required'})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'name': 'state', 'required': 'required'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'name': 'city', 'required': 'required'})
        self.fields['zipcode'].widget.attrs.update({'class': 'form-control', 'name': 'zipcode', 'required': 'required'})

class AddNewTenantForm(UserCreationForm):
    lease_start = forms.DateField()
    lease_end = forms.DateField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2','first_name', 'last_name', 'phone', 'address', 'city', 'state', 'zipcode', 'lease_start', 'lease_end']

    def __init__(self, *args, **kwargs):
        super(AddNewTenantForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control', 'name': name, 'required': 'required'})
        self.fields['lease_start'].widget.attrs.update({'class': 'datepicker-here form-control digits', 'name': 'lease_start', 'data-language': 'en'})
        self.fields['lease_end'].widget.attrs.update({'class': 'datepicker-here form-control digits', 'name': 'lease_end', 'data-language': 'en'})


