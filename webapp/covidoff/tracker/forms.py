from django import forms
from tracker.models import Device

class DeviceForm(forms.ModelForm):
	
	class Meta:
		model = Device
		fields = ['uid']

class MatchForm(forms.Form):

	matcher = forms.CharField(max_length=256, required=True)
	matchee = forms.CharField(max_length=256, required=True)

	matcher_meta = forms.CharField(max_length=2048, required=True)
	matchee_meta = forms.CharField(max_length=2048, required=True)	

	timestamp = forms.DateTimeField()
