from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from authnoop.views import CallbackView

urlpatterns = [
	path('callback/', csrf_exempt(CallbackView.as_view()), name='callback'),
]
