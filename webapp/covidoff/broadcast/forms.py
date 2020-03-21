from django import forms

class MessageForm(forms.Form):

	text = forms.CharField(widget=forms.Textarea)
	

class UserCreationForm(forms.Form):

	email = forms.EmailField()
	