from django.shortcuts import get_object_or_404
from django.views import generic
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.utils.http import is_safe_url

from .forms import SignupForm, SigninForm


User = get_user_model()


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


signup = SignupView.as_view()
confirm_email = ConfirmEmail.as_view()
check_email = CheckEmail.as_view()
