from django import forms

class LoginForm(forms.Form):

	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())
	
class RecoverForm(forms.Form):

	email = forms.EmailField()

class UserCreationForm(forms.Form):

	email = forms.EmailField()
	