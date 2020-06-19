from django import forms

class MetricsForm(forms.Form):
    aggregation = forms.CharField()
    definition = forms.IntegerField(min_value=0)

