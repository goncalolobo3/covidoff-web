from django.views.generic import TemplateView
from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from broadcast.models import Message
from broadcast.forms import MessageForm
from broadcast.forms import UserCreationForm
import nacl.encoding
import nacl.signing
import logging

logger = logging.getLogger(__name__)

class BroadcastView(TemplateView):
	template_name = 'broadcast.html'

	def post(self, request):

		form = MessageForm(request.POST)

		if not form.is_valid():
			
			return render(request, self.template_name, {
				'errors': form.errors.items()
			}, status=422)

		Message.objects.create(**{
			'text': form.cleaned_data['text'],
			'author': request.user
		})

		message = form.cleaned_data['text']

		self._encode_and_sign(message)
		self._broadcast(message)

		return redirect('broadcast_ok')

	def _encode_and_sign(self, message):
		return self._signing_key().sign(message.encode('utf-8'))

	def _signing_key(self):
		return nacl.signing.SigningKey(settings.COVIDOFF_SIGNING_KEY, nacl.encoding.HexEncoder)

	def _broadcast(self, message):

		# TODO broadcast logic
		logger.warning('Received a broadcast request, but broadcasting is not implemented yet')

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
