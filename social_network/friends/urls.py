from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RespondToFriendRequestView,
    SendFriendRequestView,
    ListReceivedPendingRequestsView,
    ListFriendsView,
)

router = DefaultRouter()
router.register(
    r"send_friend_request", SendFriendRequestView, basename="send-friend-request"
)
router.register(
    r"respond_to_friend_request",
    RespondToFriendRequestView,
    basename="respond-to-friend-request",
)
router.register(
    r"list_received_pending_request",
    ListReceivedPendingRequestsView,
    basename="list-received-pending-request",
)
router.register(
    r"list_friends",
    ListFriendsView,
    basename="list-friends",
)

urlpatterns = [
    path("", include(router.urls)),
]
