from django.urls import path
from tracker.views import MatchView

urlpatterns = [
	path('', MatchView.as_view()),
]
