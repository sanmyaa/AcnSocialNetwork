from typing import Dict
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractBaseUser


def get_tokens(user: AbstractBaseUser) -> Dict[str, str]:
    """
    Generate and return JWT tokens for a given user.
    Args:
        user (AbstractBaseUser): The user instance for which to generate tokens.
    Returns:
        Dict[str, str]: A dictionary containing the refresh and access tokens.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
