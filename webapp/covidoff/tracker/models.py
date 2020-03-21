from django.db import models
from django.utils.translation import ugettext_lazy as _

class Device(models.Model):

	uid = models.CharField(max_length=255, primary_key=True,
		help_text=_('Creation date'))

class Match(models.Model):

	matcher = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='matches_as_matcher',
		help_text=_('Matcher device'))

	matchee = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='matches_as_matchee',
		help_text=_('Matchee device'))

	matcher_meta = models.CharField(max_length=2048,
		help_text=_('Meta information associated with the matcher'))

	matchee_meta = models.CharField(max_length=2048,
		help_text=_('Meta information associated with the matchee'))

	timestamp = models.DateTimeField(
		help_text=_('Timestamp event collected at the matcher device'))

	creation_date = models.DateTimeField(auto_now_add=True,
		help_text=_('Creation date'))
	
	last_update = models.DateTimeField(auto_now=True,
		help_text=_('Last update'))
