"""
Custom authentication backend to allow login with email or username.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authentication backend that allows users to login with either
    their email address or username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        # Try to find user by email or username
        try:
            # Check if the username is actually an email
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        # Verify password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None


from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
        }
    }