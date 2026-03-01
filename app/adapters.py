from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from .authentication import get_tokens_for_user


class SocialLoginAdapter(DefaultSocialAccountAdapter):

    def get_connect_redirect_url(self, request, socialaccount):
        user = request.user
        tokens = get_tokens_for_user(user)

        return f"http://localhost:3000/auth/callback?token={tokens['access']}"