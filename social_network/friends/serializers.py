from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from accounts.serializers import UserSerializer
from social_network.errlabelscustom import FRIEND_REQUEST
from social_network.utils.serializerutils import check_request_to_self

from .models import DroppedRequest, Friendship, PendingRequest

User = get_user_model()


class FriendshipSerializer(serializers.ModelSerializer):
    """
    Serializer for Friendship model.
    """

    class Meta:
        model = Friendship
        fields = ["from_user", "to_user", "requested_at"]


class DroppedRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for DroppedRequest model.
    """

    class Meta:
        model = DroppedRequest
        fields = ["from_user", "to_user", "status", "requested_at"]


class SendFriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for sending a friend request.
    """

    class Meta:
        model = PendingRequest
        fields = ["id", "from_user", "to_user"]

    def to_internal_value(self, data):
        """
        Convert to internal representation and add user.
        """
        request = self.context.get("request")
        if request:
            data["from_user"] = request.user.pk
        return super().to_internal_value(data)

    def validate(self, attrs):
        """
        Validate the incoming data with sanity check.
        """
        data = super().validate(attrs)
        check_request_to_self(data, label=FRIEND_REQUEST)
        return data


class RespondToFriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for responding to a friend request.
    """

    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    ACTION_CHOICES = [
        (ACCEPT, "Accept Request"),
        (REJECT, "Reject Request"),
    ]
    action = serializers.ChoiceField(choices=ACTION_CHOICES, write_only=True)

    class Meta:
        model = PendingRequest
        fields = ["action"]

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Create friend or remove request based on the action.
        """
        if validated_data["action"] == self.ACCEPT:
            serializer = FriendshipSerializer(
                data={
                    "from_user": instance.from_user.pk,
                    "to_user": instance.to_user.pk,
                    "requested_at": instance.created_at,
                }
            )
        else:
            serializer = DroppedRequestSerializer(
                data={
                    "from_user": instance.from_user.pk,
                    "to_user": instance.to_user.pk,
                    "status": DroppedRequest.REJECTED,
                    "requested_at": instance.created_at,
                }
            )
        instance.delete()
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def to_representation(self, instance):
        """
        Custom representation based on result.
        """
        status = (
            "Friendship Created"
            if isinstance(instance, Friendship)
            else "Request Rejected"
        )
        return {"status": status}


class ReceivedPendingRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for received friend requests that have not been responded to.
    """

    from_user = UserSerializer(read_only=True)

    class Meta:
        model = PendingRequest
        fields = ["id", "from_user", "created_at"]


class FriendsSerializer(serializers.ModelSerializer):
    """
    Serializer for friends (people who have accepted friend requests).
    """

    to_user = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ["id", "to_user", "requested_at", "created_at"]
