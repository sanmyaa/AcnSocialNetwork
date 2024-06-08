from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoginView, RegisterView, UserListView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(r"register", RegisterView, basename="register")
router.register(r"login", LoginView, basename="login")
router.register(r"users", UserListView, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("token_refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token_verify/", TokenVerifyView.as_view(), name="token-verify"),
]
