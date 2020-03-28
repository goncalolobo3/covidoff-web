from django.test import TestCase
from django.urls import reverse
from reports.models import Device

class TestMatch(TestCase):
	fixtures = ['reports/fixtures/diagnosticchoices.json']

	def test_match(self):

		response = self.client.post(reverse('match'), {
			'matcher': '1B939BAB-410D-4D78-82FD-499D040BEF50',
			'matchee': '49F40398-29E6-4564-B4C2-8ED7740C1704',
			'latitude': '30.583330',
			'longitude': '114.266670',
			'matcher_meta': 'Matcher meta info',
			'matchee_meta': 'Matchee meta info'
		}, content_type='application/json')

		self.assertEqual(response.status_code, 200)

	def test_match_absent_arguments(self):

		response = self.client.post(reverse('match'), {
			# 'matcher': '1B939BAB-410D-4D78-82FD-499D040BEF50',
			# 'matchee': '49F40398-29E6-4564-B4C2-8ED7740C1704',
			'latitude': '30.583330',
			'longitude': '114.266670',
			'matcher_meta': 'Matcher meta info',
			'matchee_meta': 'Matchee meta info'
		}, content_type='application/json')

		self.assertEqual(response.status_code, 422)

		response = self.client.post(reverse('match'), {
			'matcher': '1B939BAB-410D-4D78-82FD-499D040BEF50',
			'matchee': '49F40398-29E6-4564-B4C2-8ED7740C1704',
			# 'latitude': '30.583330',
			# 'longitude': '114.266670',
			# 'matcher_meta': 'Matcher meta info',
			# 'matchee_meta': 'Matchee meta info'
		}, content_type='application/json')

		self.assertEqual(response.status_code, 200)

	def test_match_device_exists(self):

		uid = '1B939BAB-410D-4D78-82FD-499D040BEF50'
		arn = '6712D98F-57C9-44D9-854F-FD9A659B32AA'

		device = Device.objects.create(**{
			'uid': uid,
			'arn': arn
		})

		response = self.client.post(reverse('match'), {
			'matcher': uid,
			'matchee': '49F40398-29E6-4564-B4C2-8ED7740C1704',
		}, content_type='application/json')

		self.assertEqual(response.status_code, 200)

		# uid or arn didn't change
		self.assertEqual(device.uid, uid)
		self.assertEqual(device.arn, arn)
