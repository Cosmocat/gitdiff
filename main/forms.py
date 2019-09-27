# main.forms.py
from django import forms

class DiffForm(forms.Form):
    diff = forms.CharField(widget=forms.Textarea(attrs={"rows": 20, "cols": 80}), label='')