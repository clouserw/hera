# Use this file if you're using Hera in a django project

from django import forms


class FlushForm(forms.Form):
    flushlist = forms.CharField(widget=forms.Textarea(), required=True)
    flushprefix = forms.CharField(required=False)
