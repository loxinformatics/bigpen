from django.contrib import admin

from ..forms.contact import ContactSocialLinkForm
from ..models.contact import (
    ContactAddress,
    ContactEmail,
    ContactNumber,
    ContactSocialLink,
)
from .site import admin_site


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
