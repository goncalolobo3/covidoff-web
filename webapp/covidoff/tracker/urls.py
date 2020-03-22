from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from tracker.views import PatientView
from tracker.views import MatchView

urlpatterns = [
	path('', login_required(PatientView.as_view()), name='patient'),
	path('match/', csrf_exempt(PatientView.as_view()), name='match'),
]
