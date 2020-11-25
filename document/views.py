from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.forms import formset_factory
from django.views.generic import View, FormView, TemplateView

from .forms import CarFormSet, CarForm
from .models import Car


class CarAddView(TemplateView):
    template_name = "document/car_create.html"

    # Define method to handle GET request
    def get(self, *args, **kwargs):
        # Create an instance of the formset
        formset = CarFormSet(queryset=Car.objects.none())
        return self.render_to_response({'car_formset': formset})

    # Define method to handle POST request
    def post(self, *args, **kwargs):
        formset = CarFormSet(data=self.request.POST)

        # Check if submitted forms are valid
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy("success"))

        return self.render_to_response({'car_formset': formset})


# class CreateDocumentView(TemplateView):
#     model = Car
#     form_class = CarForm
#     template_name = 'document/create_car_document.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['car_form'] = CarForm()
#         return context
#
#     def post(self, request, *args, **kwargs):
#         form = CarForm(request.POST)
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return render(request, 'document/create_car_document.html', {'car_form': form})
#
#     def form_valid(self, form):
#         cleaned_data = form.cleaned_data
#         car = Car(name=cleaned_data['name'], number=cleaned_data['number'])
#         car.save()
#         return redirect('success')


class CreateIndexView(View):
    pass


class Success(View):

    def get(self, request, *args, **kwargs):
        return render(request, "document/success.html")

