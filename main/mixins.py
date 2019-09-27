import re
from django.http import JsonResponse
from django.shortcuts import render
from main.diffparser import parser

class AjaxFormMixin(object):
    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            self.context['results']  = parser(form.cleaned_data)
            return render(self.request, 'diffresult.html', self.context)
        else:
            return response