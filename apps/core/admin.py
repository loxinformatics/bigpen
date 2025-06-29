from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.utils.html import format_html

from .forms import (
    BaseDetailForm,
    BaseImageForm,
    ContactSocialLinkForm,
    UserChangeForm,
)
from .models import (
    BaseDetail,
    BaseImage,
    ContactAddress,
    ContactEmail,
    ContactNumber,
    ContactSocialLink,
    ListCategory,
    ListItem,
    UserRole,
)
from .site import portal_site

# ============================================================================
# BASE ADMIN
# ============================================================================


class UniqueChoiceAdminMixin(admin.ModelAdmin):
    """
    Mixin for Django admin models where the 'name' field is chosen from a unique set of
    predefined choices. This mixin restricts non-superusers from selecting or modifying
    certain 'superuser-only' choices, enforces read-only fields on editing, and disables deletion.
    """

    exclude = ("ordering",)
    list_display = ("name",)
    ordering = ("ordering",)
    superuser_only_choices = []

    def get_readonly_fields(self, request, obj=None):
        """
        Returns a list of fields to be displayed as read-only in the admin form.
        The 'name' field is read-only when editing an existing object.
        The 'ordering' field is always read-only.
        """
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj:
            readonly_fields.append("name")
        if "ordering" not in readonly_fields:
            readonly_fields.append("ordering")
        return readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        """
        Customize the form to filter out choices from the 'name' field
        that are restricted to superusers only, for non-superuser requests.
        """
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser and "name" in form.base_fields:
            form.base_fields["name"].choices = [
                choice
                for choice in form.base_fields["name"].choices
                if choice[0] not in self.superuser_only_choices
            ]
        return form

    def get_queryset(self, request):
        """
        Modify the queryset to exclude objects with names restricted to superusers
        for non-superuser users.
        """
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.exclude(name__in=self.superuser_only_choices)
        return qs

    def has_add_permission(self, request):
        """
        Determines if the user has permission to add new objects.
        Non-superusers can only add objects with 'name' choices that are not
        restricted to superusers and that are not already used.
        """
        all_choices = [c[0] for c in self.model.CHOICES]
        if not request.user.is_superuser:
            all_choices = [
                c for c in all_choices if c not in self.superuser_only_choices
            ]
        used = self.model.objects.values_list("name", flat=True)
        remaining = [c for c in all_choices if c not in used]
        return bool(remaining) and super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """
        Disable delete permission for all users.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Restrict change permission such that:
        - Only superusers can edit objects with superuser-only names.
        - Otherwise, follow the default permission logic.
        """
        if not super().has_change_permission(request, obj):
            return False
        if (
            obj
            and not request.user.is_superuser
            and obj.name in self.superuser_only_choices
        ):
            return False
        return True

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        """
        Customize the change form view to conditionally show the 'Save and add another'
        button based on whether there are any remaining allowed choices to add.
        """
        extra_context = extra_context or {}
        all_choices = [c[0] for c in self.model.CHOICES]
        if not request.user.is_superuser:
            all_choices = [
                c for c in all_choices if c not in self.superuser_only_choices
            ]
        used = self.model.objects.values_list("name", flat=True)
        extra_context["show_save_and_add_another"] = bool(set(all_choices) - set(used))
        return super().changeform_view(request, object_id, form_url, extra_context)


@admin.register(BaseDetail, site=portal_site)
class BaseDetailAdmin(UniqueChoiceAdminMixin):
    """
    Admin interface for BaseDetail model, using UniqueChoiceAdminMixin to enforce unique
    'name' choices and restrictions. Allows editing of the 'value' field inline.
    """

    form = BaseDetailForm
    list_display = ("name", "value")
    list_editable = ("value",)
    fieldsets = (("Site Detail", {"fields": ("name", "value")}),)
    superuser_only_choices = ["base_author", "base_author_url", "base_theme_color"]


@admin.register(BaseImage, site=portal_site)
class BaseImageAdmin(UniqueChoiceAdminMixin):
    """
    Admin interface for BaseImage model, using UniqueChoiceAdminMixin to enforce unique
    'name' choices. Allows editing of the 'image' field inline.
    """

    form = BaseImageForm
    list_display = ("name", "image", "description")
    list_editable = ("image",)
    fieldsets = (("Site Graphic", {"fields": ("name", "image")}),)


# ============================================================================
# CONTACT ADMIN
# ============================================================================


@admin.register(ContactSocialLink, site=portal_site)
class ContactSocialLinkAdmin(admin.ModelAdmin):
    """
    Admin interface for ContactSocialLink model, supporting listing, filtering, searching,
    and inline editing of URLs and order. Restricts the 'name' field to read-only on edit.
    """

    form = ContactSocialLinkForm
    list_display = ("name", "url", "is_active", "order")
    list_editable = ("url", "order")
    list_filter = ("is_active",)
    search_fields = ("name", "url")
    ordering = ("order",)
    fieldsets = (
        (
            "Social Media Details",
            {
                "fields": (
                    "name",
                    "url",
                )
            },
        ),
        ("Display Options", {"fields": ("is_active", "order")}),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Make the 'name' field read-only when editing an existing SocialMediaLink.
        """
        if obj:  # editing an existing object
            return ("name",)
        return ()


@admin.register(ContactNumber, site=portal_site)
class ContactNumberAdmin(admin.ModelAdmin):
    """
    Admin interface for ContactNumber model with support for listing, filtering,
    searching, ordering, and inline editing of the 'order' field.
    The 'number' field is read-only when editing an existing object.
    """

    list_display = ("number", "is_active", "is_primary", "use_for_whatsapp", "order")
    list_editable = ("order",)
    list_filter = ("is_active", "is_primary", "use_for_whatsapp")
    search_fields = ("number",)
    ordering = ("order",)
    fieldsets = (
        (
            "Phone Number Details",
            {"fields": ("number",)},
        ),
        (
            "Display Options",
            {"fields": ("is_active", "is_primary", "use_for_whatsapp", "order")},
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Make the 'number' field read-only when editing an existing PhoneNumber.
        """
        if obj:  # editing an existing object
            return ("number",)
        return ()


@admin.register(ContactEmail, site=portal_site)
class ContactEmailAdmin(admin.ModelAdmin):
    """
    Admin interface for ContactEmail model with support for listing, filtering,
    searching, ordering, and inline editing of the 'order' field.
    The 'email' field is read-only when editing an existing object.
    """

    list_display = ("email", "is_active", "is_primary", "order")
    list_editable = ("order",)
    list_filter = ("is_active", "is_primary")
    search_fields = ("email",)
    ordering = ("order",)
    fieldsets = (
        (
            "Email Address Details",
            {"fields": ("email",)},
        ),
        ("Display Options", {"fields": ("is_active", "is_primary", "order")}),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Make the 'email' field read-only when editing an existing EmailAddress.
        """
        if obj:  # editing an existing object
            return ("email",)
        return ()


@admin.register(ContactAddress, site=portal_site)
class ContactAddressAdmin(admin.ModelAdmin):
    """
    Admin interface for ContactAddress model supporting listing, filtering,
    searching, ordering, and displaying detailed address fields.
    """

    list_display = (
        "label",
        "city",
        "country",
        "use_in_contact_form",
        "is_active",
        "order",
    )
    list_editable = ("order",)
    list_filter = ("is_active", "use_in_contact_form", "country", "state_province")
    search_fields = ("label", "street_address", "city", "country")
    ordering = ("order",)

    fieldsets = (
        (
            "Address Details",
            {
                "fields": (
                    "label",
                    "building",
                    "street_address",
                    "city",
                    "state_province",
                    "postal_code",
                    "country",
                    "map_embed_url",
                )
            },
        ),
        ("Display Options", {"fields": ("is_active", "use_in_contact_form", "order")}),
    )


# ============================================================================
# LIST ADMIN
# ============================================================================
@admin.register(ListCategory, site=portal_site)
class ListCategoryAdmin(admin.ModelAdmin):
    """
    Admin for ListCategory model. Allow permissions only for superusers.
    """

    list_display = (
        "name",
        "bootstrap_icon",
        "order",
    )
    list_editable = ("order",)
    ordering = ("order",)
    search_fields = ("name",)
    fieldsets = (
        ("Category Details", {"fields": ("name",)}),
        ("Display Options", {"fields": ("bootstrap_icon", "order")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")


# Custom filter for ListItem based on category name
class CategoryNameFilter(admin.SimpleListFilter):
    title = "Category"
    parameter_name = "category_name"

    def lookups(self, request, model_admin):
        categories = set(ListCategory.objects.values_list("name", flat=True))
        return [(cat, cat) for cat in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__name=self.value())
        return queryset


@admin.register(ListItem, site=portal_site)
class ListItemAdmin(admin.ModelAdmin):
    """
    Admin for ListItem model with enhanced display, filtering,
    search, and form behavior.
    """

    list_display = (
        "name",
        "bootstrap_icon",
        "category",
        "order",
    )
    list_editable = (
        "bootstrap_icon",
        "order",
    )
    list_filter = (CategoryNameFilter, "category")
    search_fields = ("name", "description")
    ordering = ("order", "name")
    fieldsets = (
        ("Item Details", {"fields": ("name", "description", "category")}),
        ("Display Options", {"fields": ("bootstrap_icon", "order")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")

    def get_form(self, request, obj=None, **kwargs):
        """
        Remove '+' add-related button from the category field.
        """
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["category"].widget.can_add_related = False
        return form


# ============================================================================
# USER ADMIN
# ============================================================================


@admin.register(UserRole, site=portal_site)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "display_name",
        "is_default_role",
        "has_portal_access",
        "user_count",
    ]
    list_editable = ["display_name", "is_default_role"]
    list_filter = ["has_portal_access", "is_default_role"]
    search_fields = ["name", "display_name"]
    filter_horizontal = ["permissions"]  # This makes permissions easier to manage

    fieldsets = (
        ("Basic Information", {"fields": ("name", "display_name", "description")}),
        ("Role Settings", {"fields": ("has_portal_access", "is_default_role", "permissions")}),
    )
    readonly_fields = (
        "name",
        "has_portal_access",
    )

    def user_count(self, obj):
        """Show number of users with this role"""
        count = obj.user_set.count()
        if count > 0:
            return format_html(
                '<a href="{}?groups__id__exact={}">{} users</a>',
                "/admin/core/user/",
                obj.pk,
                count,
            )
        return "0 users"

    user_count.short_description = "Users"

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion via admin
        return False

    def has_add_permission(self, request, obj=None):
        # Prevent addition via admin
        return False

    def get_form(self, request, obj=None, **kwargs):
        """Customize the form to group permissions by app"""
        form = super().get_form(request, obj, **kwargs)

        # Group permissions by app for better UX
        if "permissions" in form.base_fields:
            permissions = Permission.objects.select_related("content_type").all()
            form.base_fields["permissions"].queryset = permissions.order_by(
                "content_type__app_label", "content_type__model", "codename"
            )

        return form


class BaseUserAdmin(UserAdmin):
    form = UserChangeForm
    list_display = [
        "username",
        "first_name",
        "last_name",
        "get_role_for_admin",
        "is_active",
    ]
    list_filter = ("is_active", "groups", "is_staff")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                )
            },
        ),
        (
            "Display Options",
            {"fields": ("order",)},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    readonly_fields = ("is_staff", "is_superuser")
    # Add filter_horizontal for better permission management
    filter_horizontal = ["groups"]

    def get_role_for_admin(self, obj):
        try:
            return obj.get_role()
        except Exception:
            return "Unknown"

    get_role_for_admin.short_description = "Role"
    get_role_for_admin.admin_order_field = "groups"

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
                if field not in ["is_staff", "is_superuser"]
            )

        return fieldsets
