from django.db import models
from django.utils.translation import ugettext_lazy as _

class Announcement(models.Model):

	content = models.TextField(max_length=255,
		help_text=_('Announcement content'))

	creation_date = models.DateTimeField(auto_now_add=True,
		help_text=_('Creation date'))
    
	last_update = models.DateTimeField(auto_now=True,
		help_text=_('Last update'))
