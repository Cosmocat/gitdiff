from django.shortcuts import render 

# Create your views here.
from django.views.generic import FormView

from .forms import DiffForm
from .mixins import AjaxFormMixin

class DiffFormView(AjaxFormMixin, FormView):
    form_class = DiffForm
    template_name  = 'forms/diff.html'
    success_url = '/form-success/'
    context = {}