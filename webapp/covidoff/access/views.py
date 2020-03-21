from django.views.generic import TemplateView
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.conf import settings
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib.auth import get_user_model
from access.forms import LoginForm
from access.forms import RecoverForm
from access.models import RecoveryTicket
import logging

logger = logging.getLogger(__name__)

class LoginView(TemplateView):
	template_name = 'login.html'

	def get(self, request):

		return render(request, self.template_name)

	def post(self, request):

		form = LoginForm(request.POST)

		if not form.is_valid():

			return render(request, self.template_name, {
				'errors': form.errors.items()
			})

		user = authenticate(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])

		if user is None:
			return render(request, self.template_name, {
				'errors': [('', [_('Email or password are incorrect')])]
			}, status=401)

		login(request, user)

		return redirect('/')

class LogoutView(View):

	def post(self, request):

		logout(request)

		return redirect(settings.LOGIN_URL)

class RecoverView(TemplateView):
	template_name = 'recover_password.html'

	def get(self, request):

		return render(request, self.template_name)

	def post(self, request):

		form = RecoverForm(request.POST)

		if not form.is_valid():

			return render(request, self.template_name, {
				'errors': form.errors.items()
			})

		User = get_user_model()

		try:
			user = User.objects.get(email=form.cleaned_data['email'])
		except User.DoesNotExist:
			user = None

		if user is not None:

			ticket = RecoveryTicket.objects.create(**{
				'user': user
			})

			# TODO send password recovery email with ticket.uid
			logger.warning('Sending email is not implemented yet')

		return redirect(reverse('recover_password_ok'))

class RecoverOkView(TemplateView):
	template_name = 'recover_password_ok.html'

#
# TODO Recover from email recovery ticket. Keep in mind 
#      that tickets should expire after a while
#
#
class RecoverCallbackView(TemplateView):
	template_name = 'recover_password_callback.html'

class UsersView(TemplateView):
	template_name = 'users.html'

	def get(self, request):
		pass

	def post(self, request):
		pass

	def delete(self, request):
		pass
