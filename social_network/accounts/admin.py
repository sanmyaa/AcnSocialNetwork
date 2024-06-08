from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "email",
        "name",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Dates",
            {"fields": ("last_login", "date_joined", "created_at", "modified_at")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "password2"),
            },
        ),
    )
    readonly_fields = (
        "email",
        "last_login",
        "date_joined",
        "created_at",
        "modified_at",
    )
    search_fields = ("email", "name")
    ordering = ("-id",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("email", "last_login", "date_joined", "created_at", "modified_at")
        return ()
