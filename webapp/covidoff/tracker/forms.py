from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorDict
from django.forms.utils import ErrorList
from django.core.exceptions import NON_FIELD_ERRORS
from tracker.models import Device

class DeviceForm(forms.Form):

	uid = forms.CharField(max_length=256, required=True)

class JsonForm:

	def __init__(self, data):
		self._data = data
		self._errors = None
		self.error_class = ErrorList

	@property
	def cleaned_data(self):
	
		if getattr(self, '_cleaned_data', None) is None:
			self.is_valid()

		return self._cleaned_data

	@property
	def errors(self):

		if self._errors is None:
			self._validate()

		return self._errors

	def _set_error(self):

		if self._errors is None:
			self._errors = {}
	
	def is_valid(self):
		self._validate()

		return len(self.errors) == 0

	def _validate(self):

		self._cleaned_data = {}
		self._errors = ErrorDict()

		for key, field in self.fields:

			try:
				value = self._data.get(key, None)
				value = field.to_python(value)

				self._cleaned_data[key] = value

			except ValidationError as ex:
				self.add_error(key, field, ex)

	@property
	def fields(self):

		for key in dir(self):
			field = getattr(self, key)

			if isinstance(field, forms.Field):
				yield key, field

	def add_error(self, key, field, error):

		if not isinstance(error, ValidationError):
			error = ValidationError(error)
		
		if hasattr(error, 'error_dict'):
			if field is not None:
				raise TypeError(
					"The argument `field` must be `None` when the `error` "
					"argument contains errors for the multiple fields."
				)
			else:
				error = error.error_dict
		else:
			error = {field or NON_FIELD_ERRORS: error.error_list}
			
		for field, error_list in error.items():

			if field not in self._errors:

				if field == NON_FIELD_ERRORS:
					self._errors[key] = self.error_class(error_class='nonfield')
				else:
					self._errors[key] = self.error_class()

			self._errors[key].extend(error_list)

			if key in self.cleaned_data:
				del self.cleaned_data[key]

class MatchForm(JsonForm):

	matcher = forms.CharField(max_length=256, required=True)
	matchee = forms.CharField(max_length=256, required=True)

	latitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False)
	longitude = forms.DecimalField(max_digits=9, decimal_places=6, required=False)

	matcher_meta = forms.CharField(max_length=2048, required=False)
	matchee_meta = forms.CharField(max_length=2048, required=False)	

class FindForm(forms.Form):
	
	find = forms.CharField(max_length=256, required=True)
