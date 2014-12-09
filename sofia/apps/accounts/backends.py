from django.contrib.auth.backends import ModelBackend as BaseModelBackend

from .models import User


class ModelBackend(BaseModelBackend):

    def authenticate(self, username, password=None):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

        if user and not user.check_password(password):
            user = None
        return user
