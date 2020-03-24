from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
import json

class TestCalls(TestCase):

	def test_match_view(self):

		# Government-only view
		if not settings.COVIDOFF_HEALTHCARE_DEPLOY:
			return

		data = {
			'matcher': 'matcher_id',
			'matchee': 'matchee_id',
			'timestamp': '13081238',
			'latitude': '30.5951051',	# Wuhan
			'longitude': '114.2999353',
			'matcher_meta': 'matcher_meta',
			'matcher_meta': 'matchee_meta',
		}

		response = self.client.post(reverse('match'), json.dumps(data), content_type='application/json')

		self.assertEqual(response.status_code, 200)

	def test_match_view_invalid(self):

		# Government-only view
		if not settings.COVIDOFF_HEALTHCARE_DEPLOY:
			return

		data = {
			'matcher': 'matcher_id',
			'matchee': 'matchee_id',
			'latitude': '<error>',	# Wuhan
			'longitude': '114.2999353',
			'matcher_meta': 'matcher_meta',
			'matcher_meta': 'matchee_meta',
		}

		response = self.client.post(reverse('match'), json.dumps(data), content_type='application/json')

		self.assertEqual(response.status_code, 422)

	def test_find_view(self):


		from django.urls import reverse

		print(reverse('find', args=['42', 'b821c665643ad219f538dc2db9035268']))
