from django.urls import path
from access.views import LoginView
from access.views import RecoverView
from access.views import RecoverOkView
from access.views import RecoverCallbackView
from access.views import LogoutView

urlpatterns = [
	path('login/', LoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('recover/', RecoverView.as_view(), name='recover_password'),
	path('recover/ok/', RecoverOkView.as_view(), name='recover_password_ok'),
	path('recover/callback/', RecoverCallbackView.as_view(), name='recover_password_callback')
]
