from django.urls import path
from django.contrib.auth.decorators import login_required
from tracker.views import PatientView

urlpatterns = [
	path('', login_required(PatientView.as_view()), name='patient'),
]
