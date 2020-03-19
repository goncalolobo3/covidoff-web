from django.urls import path
from announcements.views import AnnouncementView

urlpatterns = [
	path('', AnnouncementView.as_view()),
]
