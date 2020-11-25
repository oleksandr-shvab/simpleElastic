from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory, ModelForm, modelformset_factory

from .models import Car


class CarForm(ModelForm):
    name = forms.CharField(min_length=2)
    number = forms.CharField(min_length=4, max_length=4)

    class Meta:
        model = Car
        fields = ['name', 'number']


CarFormSet = modelformset_factory(Car, fields=("name", "number"), extra=1, min_num=1, validate_min=True)
