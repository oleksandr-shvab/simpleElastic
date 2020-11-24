from django import forms
from django.core.exceptions import ValidationError
from django.forms import formset_factory, ModelForm

from .models import Car


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'number']

    name = forms.CharField(min_length=2, required=True)
    number = forms.CharField(min_length=4, max_length=4, required=True)

    def clean_name(self):
        data = self.cleaned_data['name']
        if data == None:
            raise ValidationError("Enter some name")
        else:
            if len(data) < 2:
                raise ValidationError("Name mast be longer then 2 character")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data


    def clean_number(self):
        data = self.cleaned_data['number']
        if data == None:
            raise ValidationError("Enter some name")
        else:
            if len(data) < 4 or len(data) > 4:
                raise ValidationError("Name mast be 4 character length")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data


CarFormSet = formset_factory(CarForm, extra=5)
