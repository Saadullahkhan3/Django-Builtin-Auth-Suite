from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.forms import UserModel



class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # Try to find user by email
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            # Try to find user by username as fallback
            try:
                user = UserModel.objects.get(username=email)
            except UserModel.DoesNotExist:
                return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None