from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from social_network.utils.filterutils import CustomFilterSearch
from social_network.utils.paginationutils import make_paginator
from social_network.utils.throttlingutils import anon_throttle, user_throttle

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

User = get_user_model()


@permission_classes([AllowAny])
class RegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Viewset for user registration.
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    pagination_class = None
    throttle_classes = [anon_throttle(100, "min")]


@permission_classes([AllowAny])
class LoginView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Viewset for user login.
    """

    queryset = User.objects.all()
    serializer_class = LoginSerializer
    pagination_class = None
    throttle_classes = [anon_throttle(300, "min")]


@permission_classes([IsAuthenticated])
class UserListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Viewset for listing users.
    """

    queryset = None
    serializer_class = UserSerializer
    pagination_class = make_paginator(page_size=10)
    throttle_classes = [user_throttle(100, "min")]
    filter_backends = [
        CustomFilterSearch(
            query_param="filter", search_fields=["name"], filter_fields=["email"]
        ),
    ]

    def get_queryset(self):
        """
        Return a queryset of non-staff users.
        """
        return User.objects.filter(is_staff=False).exclude(pk=self.request.user.pk)
