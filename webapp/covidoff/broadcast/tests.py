from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from broadcast.models import Message

class TestBroadcast(TestCase):

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

		Message.objects.create(**{
			'author': user,
			'title': 'title-1',
			'text': 'text-1'
		})

		Message.objects.create(**{
			'author': user,
			'title': 'title-2',
			'text': 'text-2'
		})

		Message.objects.create(**{
			'author': user,
			'title': 'title-3',
			'text': 'text-3'
		})

	def test_broadcast(self):

		response = self.client.post(reverse('broadcast'), {
			'title': 'Hello world',
			'text': 'Olá, com UTF-8'
		})

		self.assertEqual(response.status_code, 302)

	def test_subscription(self):

		response = self.client.post(reverse('subscribe'), {
			'device': '588F568A-7BF5-4531-8F47-D857AD2B2833',
			'endpoint': 'arn:aws:sns:sa-east-1:494854379016:endpoint/GCM/covidoff-android/6c58628f-b073-3350-b2f3-803984511637'
		}, content_type='application/json')

