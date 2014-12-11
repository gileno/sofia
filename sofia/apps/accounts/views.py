from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import generic
from django.contrib.auth import (
    get_user_model, login, authenticate, update_session_auth_hash
)
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.conf import settings

from .forms import SignupForm, ResetPasswordForm, UpdateAccountForm
from .models import ResetPassword


User = get_user_model()


class DashboardView(generic.TemplateView):

    template_name = 'accounts/dashboard.html'


class SignupView(generic.CreateView):

    model = User
    form_class = SignupForm
    success_url = reverse_lazy('accounts:confirm_email')
    template_name = 'accounts/signup.html'


class ConfirmEmail(generic.TemplateView):

    template_name = 'accounts/confirm_email.html'


class CheckEmail(generic.TemplateView):

    template_name = 'accounts/check_email.html'

    def get_context_data(self, **kwargs):
        context = super(CheckEmail, self).get_context_data(**kwargs)
        token = self.kwargs.get('token')
        pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)
        if user.check_email(token):
            context['success'] = True
        return context


class ResetPasswordView(generic.FormView):

    form_class = ResetPasswordForm
    template_name = 'accounts/reset_password.html'

    def form_valid(self, form):
        form.reset()
        extra_context = {
            'success': True
        }
        return self.render_to_response(self.get_context_data(**extra_context))


class SetPasswordView(generic.FormView):

    form_class = SetPasswordForm
    template_name = 'accounts/set_password.html'

    _reset_password = None

    def get_reset_password(self):
        if self._reset_password is None:
            key = self.kwargs['key']
            self._reset_password = ResetPassword.objects.get(
                key=key, confirmed_on__isnull=True
            )
        return self._reset_password

    def get_form_kwargs(self):
        kwargs = super(SetPasswordView, self).get_form_kwargs()
        reset_password = self.get_reset_password()
        kwargs['user'] = reset_password.user
        return kwargs

    def form_valid(self, form):
        form.save()
        reset_password = self.get_reset_password()
        reset_password.confirmed_on = timezone.now()
        reset_password.save()
        user = authenticate(
            username=reset_password.user.username,
            password=form.cleaned_data['new_password1']
        )
        login(self.request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)


class UpdateAccountView(generic.UpdateView):

    model = User
    template_name = 'accounts/update_account.html'
    form_class = UpdateAccountForm
    success_url = reverse_lazy('accounts:update_account')

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(generic.FormView):

    template_name = 'accounts/change_password.html'

    def get_form_kwargs(self):
        kwargs = super(ChangePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_class(self):
        if self.request.user.has_usable_password():
            return PasswordChangeForm
        else:
            return SetPasswordForm

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        extra_context = {'success': True}
        return self.render_to_response(self.get_context_data(**extra_context))


dashboard = login_required(DashboardView.as_view())
signup = SignupView.as_view()
confirm_email = ConfirmEmail.as_view()
check_email = CheckEmail.as_view()
reset_password = ResetPasswordView.as_view()
set_password = SetPasswordView.as_view()
update_account = login_required(UpdateAccountView.as_view())
change_password = login_required(ChangePasswordView.as_view())
