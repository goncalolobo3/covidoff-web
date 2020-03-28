from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from reports.views import MatchView

urlpatterns = [

	path('match/', csrf_exempt(MatchView.as_view()), name='match'),

	# path('', login_required(BroadcastView.as_view()), name='broadcast'),
	# path('ok/', login_required(BroadcastOkView.as_view()), name='broadcast_ok'),
	# path('log/', login_required(BroadcastLogView.as_view()), name='broadcast_log'),
	# path('pk/', csrf_exempt(KeyView.as_view()), name='public_key'),
	# path('subscribe/', csrf_exempt(SubscriptionView.as_view()), name='subscribe')
]
