from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoginView, RegisterView, UserListView

router = DefaultRouter()
router.register(r"register", RegisterView, basename="register")
router.register(r"login", LoginView, basename="login")
router.register(r"users", UserListView, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
