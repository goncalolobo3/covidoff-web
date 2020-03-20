from django.views import View
from django.http import JsonResponse
from tracker.models import Match
from tracker.forms import MatchForm
import json

class MatchView(View):

	def put(self, request):

		try:
			body = request.body.decode('utf-8')
			body = json.loads(body)

		except json.decoder.JSONDecodeError as ex:
			return JsonResponse({ 'error': str(ex) }, status=400)

		form = MatchForm(body)

		if not form.is_valid():
			return JsonResponse(dict(form.errors.items()), status=422)

		Match.objects.create(**{
			'matcher': form.cleaned_data['matcher'],
			'matchee': form.cleaned_data['matchee']
		})

		return JsonResponse({})

