from django import forms
from covidoff.forms import JsonForm

class MatchForm(JsonForm):

	matcher = forms.CharField(max_length=256, required=True)
	matchee = forms.CharField(max_length=256, required=True)

	latitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False)
	longitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False)

	matcher_meta = forms.CharField(max_length=2048, required=False)
	matchee_meta = forms.CharField(max_length=2048, required=False)	
