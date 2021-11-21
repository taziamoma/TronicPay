from django.forms import ModelForm
from django import forms
from .models import ServiceRequests

class CreateServiceRequestForm(ModelForm):
    class Meta:
        model = ServiceRequests
        fields = ['description', 'category', 'priority']


    def __init__(self, *args, **kwargs):
        super(CreateServiceRequestForm, self).__init__(*args, **kwargs)

        self.fields['description'].widget.attrs.update({'class':'form-control', 'name': 'description'})
        self.fields['category'].widget.attrs.update({'class': 'form-select digits', 'name': 'category'})
        self.fields['priority'].widget.attrs.update({'class': 'form-select digits', 'name': 'priority'})