from django.test import TestCase
from django.conf import settings
from django.urls import reverse

class TestCalls(TestCase):

	def test_match_view(self):

		# Government-only view
		if not settings.COVIDOFF_AUTHENTICATION_DEPLOY:
			return

		self.client.post(reverse('callback'), {}, content_type='application/json')
