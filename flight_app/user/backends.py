from user.models import User
import logging

class MyAuthBackend(object):
    def authenticate(self, email, password):
        try:
            user = User.objects.get(email=email, password=password)
            if user:
                return user
            else:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(sys_id=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None