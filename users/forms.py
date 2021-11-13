from django.forms import ModelForm
from django import forms
from .common import CustomUser

class EditProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','email', 'phone','address','zipcode']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class':'form-control', 'name': 'first_name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'name': 'last_name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'name': 'email'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'name': 'phone'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'name': 'address'})
        self.fields['zipcode'].widget.attrs.update({'class': 'form-control', 'name': 'zipcode'})