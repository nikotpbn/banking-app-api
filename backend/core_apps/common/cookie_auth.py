from typing import Optional, Tuple

from django.conf import settings
from loguru import logger
from rest_framework.request import Request
from rest_framework.simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import Token

class CookieAuthentication(JWTAuthentication):
    """
    Custom authentication class that checks for a JWT in the request's cookies.
    """

    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        header = self.get_header(request)
        raw_token = None

        if header:
            raw_token = self.get_raw_token(header)
        elif settings.COOKIE_NAME in request.COOKIES:
            raw_token = request.COOKIES.get(settings.COOKIE_NAME)

        if raw_token is not None:
            try:
                validated_token = self.get_validated_toke(raw_token)
                return self.get_user(validated_token), validated_token
            except TokenError as e:
                logger.error(f"Token validation error: {e}")

        return None