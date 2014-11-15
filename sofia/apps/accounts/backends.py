from django.contrib.auth.backends import ModelBackend as BaseModelBackend

from .models import User


class ModelBackend(BaseModelBackend):

    def authenticate(self, username, password=None):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(password):
                return user
