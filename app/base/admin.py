from django.contrib import admin

from .forms import BaseOrgDetailForm, BaseOrgGraphicForm, BaseSocialMediaLinkForm
from .models import (
    EmailAddress,
    OrgDetail,
    OrgGraphic,
    PhoneNumber,
    PhysicalAddress,
    SocialMediaLink,
)


@admin.register(OrgDetail)
class SiteDetailAdmin(admin.ModelAdmin):
    form = BaseOrgDetailForm
    list_display = ("name", "value")
    list_editable = ("value",)
    list_filter = ("name",)
    search_fields = ("name", "value")
    ordering = ("name",)
    fieldsets = (
        (
            "Site Detail",
            {
                "fields": (
                    "name",
                    "value",
                )
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ("name",)
        return ()


@admin.register(OrgGraphic)
class SiteGraphicAdmin(admin.ModelAdmin):
    form = BaseOrgGraphicForm
    list_display = ("name", "image")
    list_editable = ("image",)
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    fieldsets = (
        (
            "Site Graphic",
            {
                "fields": (
                    "name",
                    "image",
                )
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ("name",)
        return ()


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    form = BaseSocialMediaLinkForm
    list_display = ("name", "url", "is_active", "order")
    list_editable = ("url", "order")
    list_filter = ("is_active", "name")
    search_fields = ("name", "url")
    ordering = ("order", "name")
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
        if obj:  # editing an existing object
            return ("name",)
        return ()


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
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
        if obj:  # editing an existing object
            return ("number",)
        return ()


@admin.register(EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
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
        if obj:  # editing an existing object
            return ("email",)
        return ()


@admin.register(PhysicalAddress)
class PhysicalAddressAdmin(admin.ModelAdmin):
    list_display = ("label", "city", "country", "is_primary", "is_active", "order")
    list_editable = ("order",)
    list_filter = ("is_active", "is_primary", "country")
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
        ("Display Options", {"fields": ("is_active", "is_primary", "order")}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ("label",)
        return ()
