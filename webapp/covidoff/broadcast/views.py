from django.views.generic import TemplateView
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.core.paginator import Paginator
from broadcast.models import Message
from broadcast.forms import MessageForm
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

		# TODO broadcast logic
		logger.warning('Received a broadcast request, but broadcasting is not implemented yet')

		return redirect('broadcast_ok')

class BroadcastOkView(TemplateView):
	template_name = 'broadcast_ok.html'

class BroadcastLogView(TemplateView):
	template_name = 'broadcast_log.html'

	def get(self, request):

		messages = Message.objects.all()
		paginator = Paginator(messages, getattr(settings, 'COVIDOFF_MESSAGES_PER_PAGE', 25))

		page_number = request.GET.get('page')
		page_object = paginator.get_page(page_number)

		return render(request, self.template_name, {
			'page': page_object
		})
