from django.views import View
from django.http import JsonResponse
from announcements.models import Announcement
from announcements.forms import AnnouncementForm
import json

class AnnouncementView(View):

	def put(self, request):

		try:
			body = request.body.decode('utf-8')
			body = json.loads(body)

		except json.decoder.JSONDecodeError as ex:
			return JsonResponse({ 'error': str(ex) }, status=400)

		form = AnnouncementForm(body)

		if not form.is_valid():
			return JsonResponse(dict(form.errors.items()), status=422)

		Announcement.objects.create(**{
			'content': form.cleaned_data['content'],
		})

		return JsonResponse({})

