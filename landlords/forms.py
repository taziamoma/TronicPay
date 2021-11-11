from django.forms import ModelForm
from django import forms
from .models import Unit

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