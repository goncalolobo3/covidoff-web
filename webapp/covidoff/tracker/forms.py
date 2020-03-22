from django import forms
from tracker.models import Device

class DeviceForm(forms.Form):

	uid = forms.CharField(max_length=256, required=True)	

class MatchForm(forms.Form):

	matcher = forms.CharField(max_length=256, required=True)
	matchee = forms.CharField(max_length=256, required=True)

	latitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False)
	longitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False)

	timestamp = forms.DateTimeField(required=True)

	matcher_meta = forms.CharField(max_length=2048, required=False)
	matchee_meta = forms.CharField(max_length=2048, required=False)	
