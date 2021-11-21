from django.forms import ModelForm
from django import forms
from .common import CustomUser

class EditProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','email', 'phone','address','city','state','zipcode']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class':'form-control', 'name': 'first_name', 'placeholder': 'Enter your first name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'name': 'last_name', 'placeholder': 'Enter your last name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'name': 'email', 'placeholder': 'Enter your email'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'name': 'phone','placeholder': 'Enter your phone number'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'name': 'address', 'placeholder': 'Enter your address'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'name': 'city', 'placeholder': 'Enter your city'})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'name': 'state', 'placeholder': 'Enter your state'})
        self.fields['zipcode'].widget.attrs.update({'class': 'form-control', 'name': 'zipcode', 'placeholder': 'Enter your zipcode'})