from django import forms

class MatchForm(forms.Form):

	matcher = forms.CharField(max_length=255, required=True)
	matchee = forms.CharField(max_length=255, required=True)
	