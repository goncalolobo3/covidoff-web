from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorDict
from django.forms.utils import ErrorList
import json

class JsonForm(forms.Form):

	def __init__(self, data, *args, **kwargs):

		try:
			data = data.decode('utf-8')
			data = json.loads(data)

			super(JsonForm, self).__init__(data, *args, **kwargs)

		except json.decoder.JSONDecodeError as ex:
			
			super(JsonForm, self).__init__({}, *args, **kwargs)

			self.add_error('', ex)
