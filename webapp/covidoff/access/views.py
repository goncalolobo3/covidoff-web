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
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from access.forms import LoginForm
from access.forms import RecoverForm
from access.forms import UserCreationForm
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
			}, status=422)

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

			self._send_recovery_email(ticket)
			
		return redirect(reverse('recover_password_ok'))

	def _send_recovery_email(self, ticket):

		# TODO
		#
		# Send the recovery email here.
		# In that email, include a URL that links back to reverse('recover_password_callback')
		# Use ticket.uid as an argument to that URL (adapt the URL to accomodate an argument).
		# That ticket.uid, should be sent in the email with the link.
		#
		# When the email is openned and the link is clicked, it redirects to reverse('recover_password_callback', uid=ticket.uid)
		#
		# You're done here.
		logger.warning('Sending email is not implemented yet')

class RecoverOkView(TemplateView):
	template_name = 'recover_password_ok.html'

class RecoverCallbackView(TemplateView):
	template_name = 'recover_password_callback.html'

	def get(self, request):

		# TODO
		#
		# This method takes an argument (uid).
		# Check that the UID is not expired (e.g. less than 10 minutes old). If is is, return 404
		#
		# Return a page to prompt for a new password
		# When the user enters the password, look for the matching UID on the database,
		# get the corresponding user (e.g. ticket.user) and use user.set_password
		#
		pass

class UsersView(TemplateView):
	template_name = 'users.html'

	def get(self, request):
		
		return render(request, self.template_name, {
			'page': self._paginator(request)
		})

	@method_decorator(user_passes_test(lambda u: u.is_superuser))
	def post(self, request):

		form = UserCreationForm(request.POST)

		if not form.is_valid():

			return render(request, self.template_name, {
				'errors': form.errors.items(),
				'page': self._paginator(request)
			}, status=422)

		user, created = get_user_model().objects.get_or_create(**{
			'email': form.cleaned_data['email'],
		})

		if created:

			user.is_active = False
			user.save()

		# New or resend invite
		if created or not user.is_active:

			self._send_invite(user)

		return render(request, self.template_name, {
			'page': self._paginator(request)
		})

	def _paginator(self, request):

		users = get_user_model().objects.all().order_by('email')
		paginator = Paginator(users, getattr(settings, 'COVIDOFF_USERS_PER_PAGE', 25))

		page_number = request.GET.get('page')
		page_object = paginator.get_page(page_number)

		return page_object

	def _send_invite(self, user):

		# TODO send invite email to user.email
		pass
