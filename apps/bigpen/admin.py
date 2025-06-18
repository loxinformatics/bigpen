from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html

from apps.core.admin import BaseUserAdmin
from apps.core.site import portal_site

from .models import Category, Item, ItemImage


class StockStatusFilter(admin.SimpleListFilter):
    """Custom filter for stock status."""

    title = "stock status"
    parameter_name = "stock_status"

    def lookups(self, request, model_admin):
        return (
            ("in_stock", "In Stock"),
            ("low_stock", "Low Stock"),
            ("out_of_stock", "Out of Stock"),
        )

    def queryset(self, request, queryset):
        from django.db import models

        if self.value() == "in_stock":
            return queryset.filter(quantity__gt=models.F("low_stock_threshold"))
        elif self.value() == "low_stock":
            return queryset.filter(
                quantity__gt=0, quantity__lte=models.F("low_stock_threshold")
            )
        elif self.value() == "out_of_stock":
            return queryset.filter(quantity=0)
        return queryset


class ItemImageInline(admin.TabularInline):
    """Inline admin for ItemImage model."""

    model = ItemImage
    extra = 1
    fields = ("image", "alt_text", "is_active")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Category, site=portal_site)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Category model with comprehensive display options,
    filtering, and organization features.
    """

    list_display = (
        "name",
        "image_preview",
        "is_active",
        "item_count",
        "order",
        "created_at",
    )
    list_editable = ("is_active", "order")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    ordering = ("order", "name")

    fieldsets = (
        ("Category Information", {"fields": ("name", "description", "image")}),
        ("Display Options", {"fields": ("bootstrap_icon", "is_active", "order")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = ("created_at", "updated_at")

    def image_preview(self, obj):
        """Display a small preview of the category image."""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url,
            )
        return "No image"

    image_preview.short_description = "Image Preview"

    def item_count(self, obj):
        """Display the number of items in this category."""
        count = obj.items.count()
        active_count = obj.get_active_items().count()
        return format_html(
            '<span title="Total: {} | Active: {}">{} items</span>',
            count,
            active_count,
            count,
        )

    item_count.short_description = "Items"


@admin.register(Item, site=portal_site)
class ItemAdmin(admin.ModelAdmin):
    """
    Admin interface for Item model with comprehensive inventory management,
    pricing display, and organization features.
    """

    list_display = (
        "name",
        "category",
        "main_image_preview",
        "current_price_display",
        "stock_status",
        "is_active",
        "is_featured",
        "order",
    )
    list_editable = ("is_active", "is_featured", "order")
    list_filter = (
        "category",
        "is_active",
        "is_featured",
        StockStatusFilter,
        "created_at",
    )
    search_fields = ("name", "description", "category__name")
    ordering = ("order", "name")

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "category", "description", "main_image")},
        ),
        (
            "Pricing",
            {
                "fields": (
                    "original_price",
                    "discount",
                    "calculated_current_price",
                    "calculated_discount_percentage",
                )
            },
        ),
        (
            "Inventory Management",
            {
                "fields": (
                    "quantity",
                    "reserved_quantity",
                    "available_quantity_display",
                    "low_stock_threshold",
                )
            },
        ),
        ("Order Constraints", {"fields": ("min_order_quantity", "max_order_quantity")}),
        (
            "Display Options",
            {"fields": ("bootstrap_icon", "is_active", "is_featured", "order")},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = (
        "calculated_current_price",
        "calculated_discount_percentage",
        "available_quantity_display",
        "created_at",
        "updated_at",
    )

    inlines = [ItemImageInline]

    def main_image_preview(self, obj):
        """Display a small preview of the main item image."""
        if obj.main_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.main_image.url,
            )
        return "No image"

    main_image_preview.short_description = "Image"

    def current_price_display(self, obj):
        """Display current price with discount information."""
        if obj.current_price is None:
            return "-"

        price_html = f"<strong>${obj.current_price:.2f}</strong>"

        if obj.discount > 0:
            price_html += f"<br><small style='color: #666;'><s>${obj.original_price:.2f}</s> (-{abs(obj.discount_percentage):.0f}%)</small>"

        return format_html(price_html)

    current_price_display.short_description = "Current Price"

    def stock_status(self, obj):
        """Display stock status with visual indicators."""
        if not obj.is_in_stock:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">Out of Stock</span>'
            )
        elif obj.is_low_stock:
            return format_html(
                '<span style="color: #fd7e14; font-weight: bold;">Low Stock ({})</span>',
                obj.available_quantity,
            )
        else:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">In Stock ({})</span>',
                obj.available_quantity,
            )

    stock_status.short_description = "Stock Status"

    def calculated_current_price(self, obj):
        """Display calculated current price in admin form."""
        if not obj or obj.current_price is None:
            return "-"
        return f"${obj.current_price:.2f}"

    calculated_current_price.short_description = "Current Price"

    def calculated_discount_percentage(self, obj):
        """Display calculated discount percentage in admin form."""
        if not obj or obj.discount_percentage == 0:
            return "No discount"
        return f"{abs(obj.discount_percentage):.1f}% off"

    calculated_discount_percentage.short_description = "Discount"

    def available_quantity_display(self, obj):
        """Display available quantity with context."""
        if not obj:
            return "-"

        available = obj.available_quantity
        reserved = obj.reserved_quantity
        total = obj.quantity

        status = f"{available} available"
        if reserved > 0:
            status += f" ({reserved} reserved)"
        status += f" of {total} total"

        return status

    available_quantity_display.short_description = "Available Stock"


@admin.register(ItemImage, site=portal_site)
class ItemImageAdmin(admin.ModelAdmin):
    """
    Admin interface for ItemImage model with image preview and organization.
    """

    list_display = ("item", "image_preview", "alt_text", "is_active", "created_at")
    list_editable = ("alt_text", "is_active")
    list_filter = ("is_active", "item__category", "created_at")
    search_fields = ("item__name", "alt_text")
    ordering = ("-created_at",)

    fieldsets = (
        ("Image Information", {"fields": ("item", "image", "alt_text")}),
        ("Display Options", {"fields": ("is_active",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = ("created_at", "updated_at")

    def image_preview(self, obj):
        """Display a preview of the item image."""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url,
            )
        return "No image"

    image_preview.short_description = "Preview"


# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0


# @admin.register(Order, site=portal_site)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ("id", "user", "created_at", "fulfilled")
#     inlines = [OrderItemInline]


@admin.register(get_user_model(), site=portal_site)
class UserAdmin(BaseUserAdmin):
    pass
