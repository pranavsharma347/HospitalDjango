from .models import CustomUser

class UserAuthenticate(object):

    def authenticate(self,email=None,password=None):
        try:
            user=CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
                return None
