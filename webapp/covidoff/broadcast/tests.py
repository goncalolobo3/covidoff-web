from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

class TestCalls(TestCase):

	def setUp(self):
		
		user = get_user_model().objects.create(**{
			'email': 'test@test.com'
		})
		user.set_password('test')
		user.save()

		response = self.client.post(reverse('login'), {
			'email': 'test@test.com',
			'password': 'test'
		})

	def test_broadcast(self):

		response = self.client.post(reverse('broadcast'), { 'text': 'Hello world' })

	# def test_subscription(self):

	# 	# Government-only view
	# 	if not settings.COVIDOFF_GOVERNMENT_DEPLOY:
	# 		return

	# 	response = self.client.post(reverse('subscribe'), {
	# 		'endpoint': 'arn:aws:sns:sa-east-1:494854379016:endpoint/GCM/covidoff-android/6c58628f-b073-3350-b2f3-803984511637'
	# 	}, content_type='application/json')

	# 	print(response)
