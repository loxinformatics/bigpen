from django.conf import settings
from django.contrib import admin
from django.contrib.admin import AdminSite as DjangoAdminSite
from django.utils.translation import gettext_lazy as _

from .forms import ContactSocialLinkForm
from .models import (
    ContactAddress,
    ContactEmail,
    ContactNumber,
    ContactSocialLink,
    ListCategory,
    ListItem,
)
from .views import signin, signout


class AdminSite(DjangoAdminSite):
    """
    Custom admin site for the organization.

    Overrides default admin login/logout URLs with custom views
    for authentication that may include branding, layout, or behavior
    tailored to the organization.
    """

    site_header = _("{} Administration").format(settings.SITE_NAME)
    site_title = _("{} Admin").format(settings.SITE_NAME)
    index_title = _("Welcome to {} Portal Manager").format(settings.SITE_NAME)

    def get_urls(self):
        """
        Returns a list of URL patterns for the custom admin site.

        Adds custom login and logout paths (handled by `signin` and `signout` views),
        and appends the default admin site URLs.
        """
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path("login/", signin, name="admin_login"),
            path("logout/", signout, name="admin_logout"),
        ]
        return custom_urls + urls


# Create custom admin site instance
admin_site = AdminSite(name="admin_site")


# ============================================================================
# CONTACT ADMIN
# ============================================================================


@admin.register(ContactSocialLink, site=admin_site)
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


@admin.register(ContactNumber, site=admin_site)
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


@admin.register(ContactEmail, site=admin_site)
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


@admin.register(ContactAddress, site=admin_site)
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
@admin.register(ListCategory, site=admin_site)
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


@admin.register(ListItem, site=admin_site)
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
