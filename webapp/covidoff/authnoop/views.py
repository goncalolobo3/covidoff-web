from django.views.generic import View
from django.http import JsonResponse

class CallbackView(View):

	def post(self, request):
		return JsonResponse({})
