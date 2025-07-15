from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from apps.core.admin.site import admin_site

from ..forms.users import UserForm


@admin.register(Group, site=admin_site)
class GroupAdmin(BaseGroupAdmin):
    pass


@admin.register(get_user_model(), site=admin_site)
class UserAdmin(BaseUserAdmin):
    form = UserForm

    def get_form(self, request, obj=None, **kwargs):
        """Override get_form to pass the current user to the form"""
        form = super().get_form(request, obj, **kwargs)

        # Create a custom form class that has access to the current user
        class FormWithUser(form):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._current_user = request.user

                # Filter groups field to hide "superuser" group for non-superusers
                if "groups" in self.fields:
                    if not request.user.is_superuser:
                        # Exclude the "superuser" group from the queryset
                        self.fields["groups"].queryset = Group.objects.exclude(
                            name="superuser"
                        )

        return FormWithUser

    readonly_fields = ("is_staff", "is_superuser")

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        if request.user.is_superuser:
            return fieldsets

        # Hide sensitive fields for non-superusers
        fieldsets = list(fieldsets)
        for name, section in fieldsets:
            section["fields"] = tuple(
                field
                for field in section["fields"]
                if field not in ["is_staff", "is_superuser", "user_permissions"]
            )

        return fieldsets


# class BaseUserAdmin(UserAdmin):
#
#     list_display = [
#         "username",
#         "first_name",
#         "last_name",
#         "get_role_for_admin",
#         "is_active",
#     ]
#     list_filter = ("is_active", "groups", "is_staff")

#     fieldsets = (
#         (None, {"fields": ("username", "password")}),
#         (
#             "Personal info",
#             {"fields": ("first_name", "last_name", "email")},
#         ),
#         (
#             "Permissions",
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                 )
#             },
#         ),
#         (
#             "Display Options",
#             {"fields": ("order",)},
#         ),
#         ("Important dates", {"fields": ("last_login", "date_joined")}),
#     )

#
#     # Add filter_horizontal for better permission management
#     filter_horizontal = ["groups"]

#     def get_role_for_admin(self, obj):
#         try:
#             return obj.get_role()
#         except Exception:
#             return "Unknown"

#     get_role_for_admin.short_description = "Role"
#     get_role_for_admin.admin_order_field = "groups"
