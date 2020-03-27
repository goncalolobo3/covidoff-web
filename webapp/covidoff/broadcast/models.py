from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Message(models.Model):

	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
	)

	title = models.TextField(max_length=255,
		help_text=_('Broadcast message title'))

	text = models.TextField(max_length=getattr(settings, 'COVIDOFF_MAXIMUM_BROADCAST_MESSAGE_SIZE', 4096),
		help_text=_('Broadcast message text'))

	creation_date = models.DateTimeField(auto_now_add=True,
		help_text=_('Creation date'))

	last_update = models.DateTimeField(auto_now=True,
		help_text=_('Last update'))

class Subscription(models.Model):

	endpoint = models.TextField(max_length=255,
		help_text=_('Subscription endpoint ARN'))

	device = models.TextField(max_length=255,
		help_text=_('Subscription device ID'))
