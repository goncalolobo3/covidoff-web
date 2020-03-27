from django.test import TestCase
from django.conf import settings
from django.urls import reverse

class TestCalls(TestCase):

	def test_match_view(self):

		self.client.post(reverse('callback'), {}, content_type='application/json')
