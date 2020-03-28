from django.db import models
from django.utils.translation import gettext as _

class DiagnosticChoicesManager(models.Manager):

	@property
	def default(self):

		# TODO language selection (using english for now)
		# TODO keep in mind that this must be done on deploy time
		return self.get(key='not', language='en')

class DiagnosticChoices(models.Model):

	objects = DiagnosticChoicesManager()

	class Meta:

		unique_together = (('key', 'language'),)

	key = models.CharField(max_length=4,
		help_text=_('Model key'))
	
	description = models.CharField(max_length=256,
		help_text=_('Diagnosis description'))

	language = models.CharField(max_length=8,
		help_text=_('Language setting'))

def _default_diagnosis():

	return DiagnosticChoices.objects.default

class Device(models.Model):

	uid = models.CharField(max_length=256, primary_key=True,
		help_text=_('Device unique identifier'))

	arn = models.TextField(max_length=256,
		help_text=_('Subscription endpoint ARN'))

	diagnosis = models.ForeignKey(DiagnosticChoices, default=_default_diagnosis, on_delete=models.PROTECT,
		help_text=_('COVID-19 Diagnosis'))

	creation_date = models.DateTimeField(auto_now_add=True,
		help_text=_('Creation date'))
	
	last_update = models.DateTimeField(auto_now=True,
		help_text=_('Last update'))

class Match(models.Model):

	matcher = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='matches_as_matcher',
		help_text=_('Matcher device'))

	matchee = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='matches_as_matchee',
		help_text=_('Matchee device'))

	latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True,
		help_text=_('GPS coordinates for the match'))

	longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True,
		help_text=_('GPS coordinates for the match'))

	matcher_meta = models.CharField(max_length=2048,
		help_text=_('Meta information associated with the matcher'))

	matchee_meta = models.CharField(max_length=2048,
		help_text=_('Meta information associated with the matchee'))

	creation_date = models.DateTimeField(auto_now_add=True,
		help_text=_('Creation date'))
	
	last_update = models.DateTimeField(auto_now=True,
		help_text=_('Last update'))
