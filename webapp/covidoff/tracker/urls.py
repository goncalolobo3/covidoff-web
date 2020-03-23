from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from tracker.views import PatientView
from tracker.views import FindView
from tracker.views import MatchView

urlpatterns = [
	path('', login_required(PatientView.as_view()), name='patient'),
	path('find/', csrf_exempt(FindView.as_view()), name='find'),
	path('match/', csrf_exempt(MatchView.as_view()), name='match'),
]
