# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import User, ResetPassword


class SigninForm(forms.Form):

    email = forms.EmailField(label=_("E-mail ou Usuário"))
    password = forms.CharField(label=_("Senha"), widget=forms.PasswordInput)

    error_messages = {
        'invalid': _(
            'Dados inválidos, preencha corretamente o e-mail ou usuário '
            'e a senha'
        ),
    }

    user = None

    def clean(self):
        if 'email' in self.cleaned_data and 'password' in self.cleaned_data:
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            self.user = authenticate(email=email, password=password)
            if self.user is None:
                raise forms.ValidationError(self.error_messages['invalid'])
        return self.cleaned_data

    def login(self, request):
        login(request, self.user)
        request.session.set_expiry(None)


class SignupForm(forms.ModelForm):

    password = forms.CharField(label=_("Senha"), widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        password = self.cleaned_data['password']
        user.set_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('name', 'email')


class UserAdminForm(forms.ModelForm):

    password = forms.CharField(
        label=_("Senha"), widget=forms.PasswordInput, required=False
    )

    def save(self, commit=True):
        user = super(UserAdminForm, self).save(commit=False)
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            if password:
                user.set_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            'name', 'email', 'verified_email', 'is_staff', 'is_superuser',
            'about', 'location'
        ]


class AdminUserChangeForm(UserChangeForm):

    pass


class AdminUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class ResetPasswordForm(forms.Form):

    email = forms.EmailField(label=_('E-mail'))

    def reset(self, send_mail=True):
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
            reset_password = ResetPassword.objects.create(user=user)
            if send_mail:
                reset_password.send_mail()
            return reset_password
        except User.DoesNotExist:
            pass


class UpdateAccountForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['name', 'username', 'about', 'location']
