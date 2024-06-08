from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from social_network.errlabelscustom import FRIEND_REQUEST, FRIENDSHIP
from social_network.utils.modelutils import TimeStampable, check_unique_relation


class PendingRequest(TimeStampable, models.Model):
    """
    Model to represent a pending friend request.
    """

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sent_active_requests",
        on_delete=models.CASCADE,
        verbose_name="sender",
        db_index=True,
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_active_requests",
        on_delete=models.CASCADE,
        verbose_name="recipient",
        db_index=True,
    )
    history = HistoricalRecords(inherit=True)

    class Meta:
        indexes = [
            models.Index(fields=["from_user", "to_user"]),
        ]
        ordering = ["-created_at"]
        verbose_name = "Pending Friend Request"
        verbose_name_plural = "Pending Friend Requests"

    def save(self, *args, **kwargs):
        """
        Save the pending request ensuring unique constraints.
        """
        check_unique_relation(self, model=Friendship, label=FRIENDSHIP)
        check_unique_relation(self, model=PendingRequest, label=FRIEND_REQUEST)
        return super().save(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the Pending Request.
        """
        return f"({self.from_user.name})  to  ({self.to_user.name})"


class Friendship(TimeStampable, models.Model):
    """
    Model to represent an accepted friendship.
    """

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="friends_by_sent_requests",
        on_delete=models.CASCADE,
        verbose_name="sender",
        db_index=True,
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="friends_by_received_requests",
        on_delete=models.CASCADE,
        verbose_name="recipient",
        db_index=True,
    )
    requested_at = models.DateTimeField()
    history = HistoricalRecords(inherit=True)

    class Meta:
        indexes = [
            models.Index(fields=["from_user", "to_user"]),
        ]
        ordering = ["-created_at"]
        verbose_name = "Friendship"
        verbose_name_plural = "Friendships"

    def save(self, *args, **kwargs):
        """
        Save the friendship ensuring unique constraints.
        """
        check_unique_relation(self, model=Friendship, label="friendship")
        check_unique_relation(self, model=PendingRequest, label="friend_request")
        return super().save(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the Friendship.
        """
        return f"({self.from_user.name})  to  ({self.to_user.name})"


class DroppedRequest(TimeStampable, models.Model):
    """
    Model to represent a dropped or rejected friend request.
    """

    REMOVED = "REMOVED"
    REJECTED = "REJECTED"
    STATUS = (
        (REMOVED, "Request Removed"),
        (REJECTED, "Request Rejected"),
    )

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sent_inactive_requests",
        verbose_name="sender",
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_inactive_requests",
        verbose_name="recipient",
        on_delete=models.CASCADE,
    )
    status = models.CharField(choices=STATUS, max_length=16)
    requested_at = models.DateTimeField()
    history = HistoricalRecords(inherit=True)

    class Meta:
        indexes = [
            models.Index(fields=["from_user", "status"]),
            models.Index(fields=["to_user", "status"]),
        ]
        ordering = ["-created_at"]
        verbose_name = "Dropped Friend Request"
        verbose_name_plural = "Dropped Friend Requests"

    def __str__(self):
        """
        Return a string representation of the Dropped Request.
        """
        return f"({self.from_user.name})  to  ({self.to_user.name})"
