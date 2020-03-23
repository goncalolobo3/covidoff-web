from django.views.generic import TemplateView
from django.views.generic import View
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from tracker.models import Device
from tracker.models import Match
from tracker.forms import DeviceForm
from tracker.forms import MatchForm
from tracker.forms import FindForm
import json
import logging

logger = logging.getLogger(__name__)

class PatientView(TemplateView):
	template_name = 'patient.html'

	def get(self, request):

		form = DeviceForm(request.GET)

		if not form.is_valid():

			# The argument is ignored
			return render(request, self.template_name, {
				'qrinfo': request.user.id,
			})

		try:

			device = Device.objects.get(uid=form.cleaned_data['uid'])

		except Device.DoesNotExist:

			# The argument is ignored
			return render(request, self.template_name, {
				'qrinfo': request.user.id,
			})

		return render(request, self.template_name, {
			'qrinfo': request.user.id,
			'device': device
		})

class FindView(View):
	
	def post(self, request):

		try:
			body = request.body.decode('utf-8')
			body = json.loads(body)

		except json.decoder.JSONDecodeError as ex:
			return JsonResponse({ 'error': str(ex) }, status=400)

		form = FindForm(body)

		if not form.is_valid():
			return JsonResponse(dict(form.errors.items()), status=422)

		# 
		find = forms.cleaned_data['find']

		return JsonResponse({})

		
class MatchView(View):

	def post(self, request):

		try:
			body = request.body.decode('utf-8')
			body = json.loads(body)

		except json.decoder.JSONDecodeError as ex:
			return JsonResponse({ 'error': str(ex) }, status=400)

		form = MatchForm(body)

		if not form.is_valid():
			return JsonResponse(dict(form.errors.items()), status=422)

		match = Match.objects.create(**{
			'matcher': Device.objects.get_or_create(uid=form.cleaned_data['matcher'])[0],
			'matchee': Device.objects.get_or_create(uid=form.cleaned_data['matchee'])[0],
			'latitude': form.cleaned_data['latitude'],
			'longitude': form.cleaned_data['longitude'],
			'timestamp': timezone.now(),
			'matcher_meta': form.cleaned_data['matcher_meta'],
			'matchee_meta': form.cleaned_data['matchee_meta'],
		})

		return JsonResponse({})

# TODO Accept in batches
