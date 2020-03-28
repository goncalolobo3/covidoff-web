from django.views.generic import TemplateView
from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.dateformat import format
from broadcast.models import Message
from broadcast.models import Subscription
from broadcast.forms import MessageForm
from broadcast.forms import UserCreationForm
from broadcast.forms import SubscriptionForm
import nacl.encoding
import nacl.signing
import logging
import boto3
import json

logger = logging.getLogger(__name__)

def _encode_and_sign(obj):

	formatted = "%d\n%s\n%s\n%s\n%s" % (obj.id, obj.title, obj.text, format(obj.creation_date, 'U'), 'gov')

	return _signing_key().sign(formatted.encode('utf-8'))

def _signing_key():

	if settings.COVIDOFF_SIGNING_KEY is None:
		raise Exception("COVIDOFF_SIGNING_KEY is not configured as an env variable. Configure it in order to broadcast messages.")

	return nacl.signing.SigningKey(settings.COVIDOFF_SIGNING_KEY, nacl.encoding.HexEncoder)

def _build_message(obj):

	return {

		'id': obj.id,
		'entity': 'gov',
		'title': obj.title,
		'text': obj.text,
		'time': format(obj.creation_date, 'U'),
		'sign': _encode_and_sign(obj).signature.hex()
	}

class SubscriptionView(View):

	def post(self, request):

		form = SubscriptionForm(request.body)

		if not form.is_valid():
			return JsonResponse(dict(form.errors.items()), status=422)

		endpoint = form.cleaned_data['endpoint']
		topic = self.topic

		client = boto3.client('sns', region_name='sa-east-1')

		try:

			subscription = client.subscribe(
				Protocol='application',
				Endpoint=endpoint,
				TopicArn=self.topic
			)

			Subscription.objects.create(**{
				'device': form.cleaned_data['device'],
				'endpoint': endpoint
			})

		except Exception as ex:

			return JsonResponse({
				'errors': [str(ex)]
			}, status=422)

		return JsonResponse({
			'pk': getattr(settings, 'COVIDOFF_VERIFY_KEY', None) or self._raise(ImproperlyConfigured('COVIDOFF_VERIFY_KEY is not set')),
			'messages': [_build_message(message) for message in Message.objects.all()]
		})

	@property
	def topic(self):
		return getattr(settings, 'COVIDOFF_SNS_TOPIC_ARN', None) or self._raise(ImproperlyConfigured('COVIDOFF_SNS_TOPIC_ARN is not set'))

	def _raise(self, message):
		raise ex
	
class BroadcastView(TemplateView):
	template_name = 'broadcast.html'

	def post(self, request):

		form = MessageForm(request.POST)

		if not form.is_valid():
			
			return render(request, self.template_name, {
				'errors': form.errors.items()
			}, status=422)

		obj = Message.objects.create(**{
			'title': form.cleaned_data['title'],
			'text': form.cleaned_data['text'],
			'author': request.user
		})

		self._broadcast(self._encode_obj(obj))

		return redirect('broadcast_ok')

	def _encode_obj(self, obj):

		return json.dumps(_build_message(obj), separators=(',', ':'))

	def _broadcast(self, message):

		# Sao Paulo
		client = boto3.client('sns', region_name='sa-east-1')

		# See: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformEndpoint.publish
		client.publish(
			TargetArn=settings.COVIDOFF_SNS_TOPIC_ARN,
			Message=message
		)

class KeyView(View):

	def get(self, request):

		return JsonResponse({ 'pk': settings.COVIDOFF_VERIFY_KEY.decode('utf-8') })

class BroadcastOkView(TemplateView):
	template_name = 'broadcast_ok.html'

class BroadcastLogView(TemplateView):
	template_name = 'broadcast_log.html'

	def get(self, request):

		return render(request, self.template_name, {
			'page': self._paginator(request)
		})

	def _paginator(self, request):

		messages = Message.objects.all().order_by('-creation_date')
		paginator = Paginator(messages, getattr(settings, 'COVIDOFF_MESSAGES_PER_PAGE', 25))

		page_number = request.GET.get('page')
		page_object = paginator.get_page(page_number)

		return page_object
