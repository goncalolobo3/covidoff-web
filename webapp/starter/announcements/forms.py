from django import forms

class AnnouncementForm(forms.Form):

	content = forms.CharField(max_length=2048, required=True)
	