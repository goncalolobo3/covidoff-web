from django import forms
from covidoff.forms import JsonForm

class MessageForm(forms.Form):

	title = forms.CharField()
	text = forms.CharField(widget=forms.Textarea)
	
class UserCreationForm(forms.Form):

	email = forms.EmailField()
	
class SubscriptionForm(JsonForm):
	
	endpoint = forms.CharField()
	device = forms.CharField()
	