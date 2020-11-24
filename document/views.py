from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.urls import reverse
from django.forms import formset_factory
from django.views.generic import View, FormView, DetailView, CreateView

from .forms import CarFormSet, CarForm
from .models import Car


class AddDocumentView(FormView):
    template_name = 'document/add_document.html'
    form_class = CarFormSet

    def form_valid(self, form):
        response = super().form_valid(form)
        cleaned_data = form.cleaned_data
        for data in cleaned_data:
            if data:
                car = Car(name=data['name'], number=data['number'])
                car.save()

        return response

    def get_success_url(self):
        return reverse('success')



class CreateIndexView(View):
    pass


class Success(View):

    def get(self, request, *args, **kwargs):
        return render(request, "document/success.html")

