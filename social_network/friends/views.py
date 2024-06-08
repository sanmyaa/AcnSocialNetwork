from rest_framework import mixins, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from social_network.utils.paginationutils import make_paginator
from social_network.utils.throttlingutils import user_throttle

from .models import Friendship, PendingRequest
from .serializers import (
    RespondToFriendRequestSerializer,
    SendFriendRequestSerializer,
    ReceivedPendingRequestSerializer,
    FriendsSerializer,
)


@permission_classes([IsAuthenticated])
class SendFriendRequestView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Viewset for sending a friend request.
    """

    queryset = PendingRequest.objects.all()
    serializer_class = SendFriendRequestSerializer
    pagination_class = None
    throttle_classes = [user_throttle(30, "min")]


@permission_classes([IsAuthenticated])
class RespondToFriendRequestView(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Viewset for responding to a friend request.
    """

    queryset = None
    serializer_class = RespondToFriendRequestSerializer
    pagination_class = None
    throttle_classes = [user_throttle(100, "min")]
    http_method_names = ["put"]

    def get_queryset(self):
        """
        Return friend requests made to this specific user.
        """
        user = self.request.user
        return PendingRequest.objects.filter(to_user=user)


@permission_classes([IsAuthenticated])
class ListReceivedPendingRequestsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Viewset for listing received pending friend requests.
    """

    queryset = None
    serializer_class = ReceivedPendingRequestSerializer
    pagination_class = None
    throttle_classes = [user_throttle(100, "min")]

    def get_queryset(self):
        """
        Return friend requests made to this specific user.
        """
        user = self.request.user
        return PendingRequest.objects.filter(to_user=user)


@permission_classes([IsAuthenticated])
class ListFriendsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Viewset for listing friends created through outgoing requests.
    """

    queryset = None
    serializer_class = FriendsSerializer
    pagination_class = None
    throttle_classes = [user_throttle(100, "min")]

    def get_queryset(self):
        """
        Return friends created through outgoing requests of this user.
        """
        user = self.request.user
        return Friendship.objects.filter(from_user=user)
