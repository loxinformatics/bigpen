from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeAdminForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeAdminForm
    model = CustomUser
    list_display = [
        "username",
        "email",
    ]

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            "Profile",
            {"fields": ("image", "first_name", "last_name", "position", "description")},
        ),
        ("Social Media", {"fields": ("facebook", "twitter", "instagram", "linkedin")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
