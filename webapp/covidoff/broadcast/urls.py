from django.urls import path
from django.contrib.auth.decorators import login_required
from broadcast.views import BroadcastView
from broadcast.views import BroadcastOkView
from broadcast.views import BroadcastLogView

urlpatterns = [
	path('', login_required(BroadcastView.as_view()), name='broadcast'),
	path('ok/', login_required(BroadcastOkView.as_view()), name='broadcast_ok'),
	path('log/', login_required(BroadcastLogView.as_view()), name='broadcast_log')
]
