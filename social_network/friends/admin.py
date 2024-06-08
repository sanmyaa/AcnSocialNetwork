from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from social_network.utils.filterutils import admin_list_filter

from .models import DroppedRequest, Friendship, PendingRequest


@admin.register(PendingRequest)
class PendingRequestAdmin(SimpleHistoryAdmin):
    list_display = ("id", "from_user", "to_user", "created_at")
    search_fields = (
        "from_user__username",
        "from_user__email",
        "to_user__username",
        "to_user__email",
    )
    list_filter = (
        "created_at",
        admin_list_filter(title="sender", field_name="from_user"),
        admin_list_filter(title="recipient", field_name="to_user"),
    )
    autocomplete_fields = ("from_user", "to_user")
    ordering = ("-id",)


@admin.register(Friendship)
class FriendshipAdmin(SimpleHistoryAdmin):
    list_display = ("id", "from_user", "to_user", "requested_at", "created_at")
    search_fields = (
        "from_user__username",
        "from_user__email",
        "to_user__username",
        "to_user__email",
    )
    list_filter = (
        "requested_at",
        "created_at",
        admin_list_filter(title="sender", field_name="from_user"),
        admin_list_filter(title="recipient", field_name="to_user"),
    )
    autocomplete_fields = ("from_user", "to_user")
    ordering = ("-id",)


@admin.register(DroppedRequest)
class DroppedRequestAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "from_user",
        "to_user",
        "status",
        "requested_at",
        "created_at",
    )
    search_fields = (
        "from_user__username",
        "from_user__email",
        "to_user__username",
        "to_user__email",
    )
    list_filter = (
        "status",
        "requested_at",
        "created_at",
        admin_list_filter(title="sender", field_name="from_user"),
        admin_list_filter(title="recipient", field_name="to_user"),
    )
    autocomplete_fields = ("from_user", "to_user")
    ordering = ("-id",)
