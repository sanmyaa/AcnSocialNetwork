from typing import Type

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

DEFAULT_LIMIT = 500
DEFAULT_PERIOD = "day"


def user_throttle(
    limit: int = DEFAULT_LIMIT, period: str = DEFAULT_PERIOD
) -> Type[UserRateThrottle]:
    """
    Create a custom user rate throttle class.
    Args:
        limit (int, optional): The rate limit for the throttle.
        period (str, optional): The period for the rate limit.
    Returns:
        Type[UserRateThrottle]: The custom user rate throttle class.
    """
    return type(
        "CustomUserThrottle", (UserRateThrottle,), {"rate": f"{limit}/{period}"}
    )


def anon_throttle(
    limit: int = DEFAULT_LIMIT, period: str = DEFAULT_PERIOD
) -> Type[AnonRateThrottle]:
    """
    Create a custom rate throttle class for anonymous users.
    Args:
        limit (int, optional): The rate limit for the throttle.
        period (str, optional): The period for the rate limit.
    Returns:
        Type[AnonRateThrottle]: The custom rate throttle class for anonymous users.
    """
    return type(
        "CustomAnonThrottle", (AnonRateThrottle,), {"rate": f"{limit}/{period}"}
    )
