from flight_app.user.models import User
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