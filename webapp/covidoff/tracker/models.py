from django.db import models
from django.utils.translation import ugettext_lazy as _

class DiagnosisChoices(models.Model):

	key = models.CharField(max_length=16,
		help_text=_('Model key'))
	
	description = models.CharField(max_length=256,
		help_text=_('Diagnosis description'))

	language = models.CharField(max_length=8,
		help_text=_('Language setting'))

	trigger = models.BooleanField(
		help_text=_('Whether the diagnosis triggers warnings'))

class Device(models.Model):

	uid = models.CharField(max_length=255, primary_key=True,
		help_text=_('Creation date'))

	diagnosis = models.ForeignKey(DiagnosisChoices, on_delete=models.CASCADE,
		help_text=_('Diagnosis'))

class Match(models.Model):

	matcher = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='matches_as_matcher',
		help_text=_('Matcher device'))

	matchee = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='matches_as_matchee',
		help_text=_('Matchee device'))

	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True,
		help_text=_('GPS coordinates for the match'))

	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True,
		help_text=_('GPS coordinates for the match'))

	timestamp = models.DateTimeField(
		help_text=_('Timestamp event collected at the matcher device'))

	matcher_meta = models.CharField(max_length=2048,
		help_text=_('Meta information associated with the matcher'))

	matchee_meta = models.CharField(max_length=2048,
		help_text=_('Meta information associated with the matchee'))

	creation_date = models.DateTimeField(auto_now_add=True,
		help_text=_('Creation date'))
	
	last_update = models.DateTimeField(auto_now=True,
		help_text=_('Last update'))
