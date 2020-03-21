from django.views import View
from django.http import JsonResponse
from announcements.models import Announcement
from announcements.forms import AnnouncementForm
from django.core.paginator import Paginator
from django.shortcuts import render
import json

class AnnouncementView(View):

	def put(self, request):

		# TODO not JSON
		try:
			body = request.body.decode('utf-8')
			body = json.loads(body)

		except json.decoder.JSONDecodeError as ex:
			return JsonResponse({ 'error': str(ex) }, status=400)

		form = AnnouncementForm(body)

		if not form.is_valid():
			return JsonResponse(dict(form.errors.items()), status=422)

		announcement = Announcement.objects.create(**{
			'content': form.cleaned_data['content'],
		})

		# Spread the word
		broadcast_announcement(announcement)

		return JsonResponse({})

	def get(self, request):

		announcements = Announcement.objects.all()
		paginator = Paginator(announcements, 25)	# TODO hardcoded

		page_num = request.GET.get('page')
		page_obj = paginator.get_page(page_num)

		return render(request, 'announcement_list.html', {
			'page_obj': page_obj
		})

def broadcast_announcement(content):

	# TODO Broadcast announcements here
	pass
