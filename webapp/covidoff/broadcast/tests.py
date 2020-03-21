from django.views.generic import TemplateView

class BroadcastView(TemplateView):
	template_name = 'broadcast.html'
