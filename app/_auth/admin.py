from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User, UserGroup

# Unregister the default Group model to use the custom UserGroup admin
admin.site.unregister(Group)


@admin.register(UserGroup)
class UserGroupAdmin(GroupAdmin):
    """
    Custom admin for UserGroup (proxy for Group).
    - Makes 'name' readonly for protected groups.
    - Prevents deletion of protected groups.
    - Adds 'is_default_group' to the list display.
    """

    def get_readonly_fields(self, request, obj=None):
        # Make 'name' readonly if the group is protected
        if obj and obj.is_protected():
            return ["name"] + list(self.readonly_fields)
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of protected groups
        if obj and obj.is_protected():
            return False
        return super().has_delete_permission(request, obj)

    def get_list_display(self, request):
        # Add 'is_default_group' to the admin list display
        return list(super().get_list_display(request)) + ["is_default_group"]


# Custom forms for handling PhoneNumberField
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert PhoneNumberField to CharField in the form
        if "username" in self.fields:
            self.fields["username"] = forms.CharField(
                label=_("Phone Number"),
                max_length=20,
                help_text=_(
                    "Enter a valid phone number in E.164 format (+12345678901)."
                ),
                required=True,
            )
            # Pre-format the initial value
            if self.instance and self.instance.pk:
                self.fields["username"].initial = str(self.instance.username)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert PhoneNumberField to CharField in the form
        if "username" in self.fields:
            self.fields["username"] = forms.CharField(
                label=_("Phone Number"),
                max_length=20,
                help_text=_(
                    "Enter a valid phone number in E.164 format (+12345678901)."
                ),
                required=True,
            )

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    """
    Custom admin for User model.
    - Removes 'user_permissions' field (permissions should be managed via groups).
    - Organizes fields into sections: Profile, Socials, Permissions, Important Dates.
    - Allows inline editing of title, first_name, last_name in the list view.
    - Restricts certain fields for non-superusers.
    """

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    fieldsets = (
        (
            "",
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (
            "PROFILE",
            {
                "fields": (
                    "image",
                    "title",
                    "email",
                    "first_name",
                    "last_name",
                    "description",
                )
            },
        ),
        (
            "SOCIALS",
            {
                "fields": (
                    "twitter_x",
                    "facebook",
                    "instagram",
                    "linkedin",
                    "github",
                    "youtube",
                    "website",
                )
            },
        ),
        (
            "PERMISSIONS",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                )
            },
        ),
        (
            "IMPORTANT DATES",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    # Customize the add form layout
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )

    # Display these fields in the user list view
    list_display = ["username", "title", "first_name", "last_name"]
    # Make username a clickable link in the list view
    list_display_links = ["username"]
    # Allow inline editing of these fields in the list view
    list_editable = ["title", "first_name", "last_name"]
    # Add filter by groups in the list view
    list_filter = ("groups",)

    def get_fieldsets(self, request, obj=None):
        """
        Customize fieldsets based on user permissions.
        Non-superusers see fewer fields (no is_superuser, is_staff, groups, description).
        """
        fieldsets = super().get_fieldsets(request, obj)

        if request.user.is_superuser:
            return fieldsets

        # Remove the fields you don't want to show for non-superusers
        fieldsets = list(fieldsets)

        for name, section in fieldsets:
            section["fields"] = tuple(
                field
                for field in section["fields"]
                if field
                not in [
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "description",
                ]
            )

        return fieldsets
