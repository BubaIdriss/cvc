#from django.contrib.auth.backends import ModelBackend
#from django.contrib.auth import get_user_model
#
#class EmailBackend(ModelBackend):
#    """
#    Custom backend to authenticate users using their email instead of username.
#    """
#    def authenticate(self, request, username=None, password=None, **kwargs):
#        UserModel = get_user_model()
#        try:
#            # We treat the username parameter as the email in this case
#            user = UserModel.objects.get(email=username)
#        except UserModel.DoesNotExist:
#            return None
#
#        # Check if the password is correct
#        if user.check_password(password) and self.user_can_authenticate(user):
#            return user
#        return None
#
#
## Generate Token
#from django.contrib.auth.base_user import AbstractBaseUser
#from django.contrib.auth.tokens import PasswordResetTokenGenerator
#import six
#
#class TokenGenerator(PasswordResetTokenGenerator):
#    #PasswordGenerator._make_hash_value(user, timestamp)
#    def _make_hash_value(self, user, timestamp):
#        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
#    
#generate_token = TokenGenerator() 