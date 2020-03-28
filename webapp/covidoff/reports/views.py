from django.views.generic import View
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.utils.dateformat import format
from reports.forms import MatchForm
from reports.models import Match
from reports.models import Device

def _format_match(obj):

	return {
		'id': obj.id,
		'matcher': obj.matcher.uid,
		'matchee': obj.matchee.uid,
		'latitude': obj.latitude,
		'longitude': obj.longitude,
		'matcher_meta': obj.matcher_meta,
		'matchee_meta': obj.matchee_meta,
		'timestamp': format(obj.creation_date, 'U')
	}

class MatchView(View):

	def post(self, request):

		form = MatchForm(request.body)

		if not form.is_valid():
			return JsonResponse(dict(form.errors.items()), status=422)

		matcher, _ = Device.objects.get_or_create(**{
			'uid': form.cleaned_data['matcher'],
		})
		
		matchee, _ = Device.objects.get_or_create(**{
			'uid': form.cleaned_data['matchee'],
		})

		match = Match.objects.create(**{
			'matcher': matcher,
			'matchee': matchee,
			'latitude': form.cleaned_data['latitude'],
			'longitude': form.cleaned_data['longitude'],
			'matcher_meta': form.cleaned_data['matcher_meta'],
			'matchee_meta': form.cleaned_data['matchee_meta']
		})

		return JsonResponse(_format_match(match))

