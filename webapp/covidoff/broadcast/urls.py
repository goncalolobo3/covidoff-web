from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from broadcast.views import BroadcastView
from broadcast.views import BroadcastOkView
from broadcast.views import BroadcastLogView
from broadcast.views import KeyView
from broadcast.views import SubscriptionView

urlpatterns = [
	path('', login_required(BroadcastView.as_view()), name='broadcast'),
	path('ok/', login_required(BroadcastOkView.as_view()), name='broadcast_ok'),
	path('log/', login_required(BroadcastLogView.as_view()), name='broadcast_log'),
	path('pk/', csrf_exempt(KeyView.as_view()), name='public_key'),
	path('subscribe/', csrf_exempt(SubscriptionView.as_view()), name='subscribe')
]
