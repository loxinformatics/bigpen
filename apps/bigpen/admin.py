from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.admin import BaseUserAdmin
from apps.core.site import portal_site

from .models import Category, Item, ItemImage, Order, OrderItem


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


class OrderStatusFilter(admin.SimpleListFilter):
    """Custom filter for order status."""

    title = "order status"
    parameter_name = "order_status"

    def lookups(self, request, model_admin):
        return (
            ("pending", "Pending"),
            ("assigned", "Assigned"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
            ("unassigned", "Unassigned Orders"),
        )

    def queryset(self, request, queryset):
        if self.value() == "unassigned":
            return queryset.filter(assigned_to__isnull=True, status="pending")
        elif self.value():
            return queryset.filter(status=self.value())
        return queryset


class ItemImageInline(admin.TabularInline):
    """Inline admin for ItemImage model."""

    model = ItemImage
    extra = 1
    fields = ("image", "alt_text", "is_active")
    readonly_fields = ("created_at", "updated_at")


class OrderItemInline(admin.TabularInline):
    """Inline admin for OrderItem model."""

    model = OrderItem
    extra = 0
    fields = ("item", "quantity", "price_at_time", "total_price_display")
    readonly_fields = ("total_price_display",)
    autocomplete_fields = ("item",)

    def total_price_display(self, obj):
        """Display total price for this order item."""
        if obj and hasattr(obj, "total_price") and obj.total_price:
            try:
                # Convert to string first to avoid SafeString issues
                price = float(obj.total_price)
                return f"${price:.2f}"
            except (ValueError, TypeError):
                return "-"
        return "-"

    total_price_display.short_description = "Total Price"


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


@admin.register(Order, site=portal_site)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for Order model with staff assignment and order management.
    """

    list_display = (
        "id",
        "user",
        "status_display",
        "assigned_to_display",
        "total_items_display",
        "total_price_display",
        "created_at",
        "fulfilled",
    )
    list_editable = ("fulfilled",)
    list_filter = (
        OrderStatusFilter,
        "fulfilled",
        "assigned_to",
        "created_at",
        "assigned_at",
    )
    search_fields = (
        "id",
        "user__username",
        "user__email",
        "notes",
        "assigned_to__username",
    )
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Order Information",
            {"fields": ("user", "status", "fulfilled", "notes")},
        ),
        (
            "Staff Assignment",
            {
                "fields": ("assigned_to", "assigned_at"),
                "description": "Assign orders to staff members for processing.",
            },
        ),
        (
            "Order Summary",
            {
                "fields": ("total_items_summary", "total_price_summary"),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at",), "classes": ("collapse",)},
        ),
    )

    readonly_fields = (
        "created_at",
        "assigned_at",
        "total_items_summary",
        "total_price_summary",
    )

    inlines = [OrderItemInline]
    actions = ["assign_to_me", "unassign_orders", "mark_completed", "mark_in_progress"]

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related("user", "assigned_to")

    def status_display(self, obj):
        """Display order status with color coding."""
        status_colors = {
            "pending": "#ffc107",  # Warning yellow
            "assigned": "#17a2b8",  # Info blue
            "in_progress": "#007bff",  # Primary blue
            "completed": "#28a745",  # Success green
            "cancelled": "#dc3545",  # Danger red
        }

        color = status_colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display().upper(),
        )

    status_display.short_description = "Status"

    def assigned_to_display(self, obj):
        """Display assigned staff member with visual indicator."""
        if obj.assigned_to:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">👤 {}</span>',
                obj.assigned_to.username,
            )
        return format_html('<span style="color: #dc3545;">Unassigned</span>')

    assigned_to_display.short_description = "Assigned To"

    def total_items_display(self, obj):
        """Display total number of items in the order."""
        try:
            total = obj.get_total_items()
            return f"{total} items"
        except Exception:
            return "0 items"

    total_items_display.short_description = "Items"

    def total_price_display(self, obj):
        """Display total price of the order."""
        try:
            total = obj.get_total_price()
            if total is None or total == 0:
                return "$0.00"
            # Convert to float to ensure it's a number, not SafeString
            price = float(total)
            return f"${price:.2f}"
        except (ValueError, TypeError, AttributeError):
            return "$0.00"

    total_price_display.short_description = "Total Price"

    def total_items_summary(self, obj):
        """Display detailed items summary."""
        if not obj.pk:
            return "Save order first to see items summary"

        items = obj.order_items.all()
        if not items:
            return "No items in this order"

        summary = []
        for item in items:
            summary.append(f"• {item.quantity}× {item.item.name}")

        return format_html("<br>".join(summary))

    total_items_summary.short_description = "Items Summary"

    def total_price_summary(self, obj):
        """Display detailed price breakdown."""
        if not obj.pk:
            return "Save order first to see price summary"

        try:
            total = obj.get_total_price()
            item_count = obj.get_total_items()

            if total is None:
                total = 0

            # Convert to float to avoid SafeString issues
            price = float(total)
            return f"Total: ${price:.2f} ({item_count} items)"
        except (ValueError, TypeError, AttributeError):
            return "Total: $0.00 (0 items)"

    total_price_summary.short_description = "Price Summary"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter assigned_to field to only show staff members."""
        if db_field.name == "assigned_to":
            User = get_user_model()
            # Filter to only staff members based on your role system
            # Users with staff_admin or manager_admin roles, or is_staff=True
            kwargs["queryset"] = User.objects.filter(
                models.Q(groups__name__in=["staff_admin", "manager_admin"])
                | models.Q(is_staff=True)
            ).distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def assign_to_me(self, request, queryset):
        """Action to assign selected orders to the current user."""
        # Check if current user can be assigned orders (has staff role or is_staff)
        user_can_be_assigned = (
            request.user.has_role("staff_admin")
            or request.user.has_role("manager_admin")
            or request.user.is_staff
        )

        if not user_can_be_assigned:
            self.message_user(
                request, "Only staff members can be assigned orders.", level="ERROR"
            )
            return

        assigned_count = 0
        for order in queryset:
            if order.can_be_assigned_to(request.user):
                try:
                    order.assign_to_staff(request.user)
                    assigned_count += 1
                except ValidationError as e:
                    self.message_user(
                        request, f"Error assigning order {order.id}: {e}", level="ERROR"
                    )

        if assigned_count:
            self.message_user(
                request, f"Successfully assigned {assigned_count} orders to you."
            )
        else:
            self.message_user(request, "No orders could be assigned.", level="WARNING")

    assign_to_me.short_description = "Assign selected orders to me"

    def unassign_orders(self, request, queryset):
        """Action to unassign selected orders."""
        unassigned_count = 0
        for order in queryset.filter(assigned_to__isnull=False):
            order.unassign_order()
            unassigned_count += 1

        if unassigned_count:
            self.message_user(
                request, f"Successfully unassigned {unassigned_count} orders."
            )
        else:
            self.message_user(
                request, "No assigned orders were selected.", level="WARNING"
            )

    unassign_orders.short_description = "Unassign selected orders"

    def mark_completed(self, request, queryset):
        """Action to mark selected orders as completed."""
        updated = queryset.update(status="completed", fulfilled=True)
        self.message_user(
            request, f"Successfully marked {updated} orders as completed."
        )

    mark_completed.short_description = "Mark selected orders as completed"

    def mark_in_progress(self, request, queryset):
        """Action to mark selected orders as in progress."""
        updated = queryset.update(status="in_progress")
        self.message_user(
            request, f"Successfully marked {updated} orders as in progress."
        )

    mark_in_progress.short_description = "Mark selected orders as in progress"


@admin.register(OrderItem, site=portal_site)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin interface for OrderItem model with pricing and inventory details.
    """

    list_display = (
        "order_id_display",
        "item",
        "quantity",
        "price_at_time_display",
        "total_price_display",
        "order_status",
    )
    list_filter = ("order__status", "item__category", "order__created_at")
    search_fields = (
        "order__id",
        "item__name",
        "order__user__username",
        "order__user__email",
    )
    ordering = ("-order__created_at",)
    autocomplete_fields = ("order", "item")

    fieldsets = (
        (
            "Order Item Information",
            {"fields": ("order", "item", "quantity")},
        ),
        (
            "Pricing",
            {"fields": ("price_at_time", "calculated_total_price")},
        ),
    )

    readonly_fields = ("calculated_total_price",)

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return (
            super().get_queryset(request).select_related("order", "item", "order__user")
        )

    def order_id_display(self, obj):
        """Display order ID with link."""
        return format_html(
            '<a href="/admin/shop/order/{}/change/">Order #{}</a>',
            obj.order.id,
            obj.order.id,
        )

    order_id_display.short_description = "Order"

    def price_at_time_display(self, obj):
        """Display price at time of order."""
        if obj.price_at_time:
            try:
                price = float(obj.price_at_time)
                return f"${price:.2f}"
            except (ValueError, TypeError):
                return "-"
        return "-"

    price_at_time_display.short_description = "Unit Price"

    def total_price_display(self, obj):
        """Display total price for this order item."""
        try:
            total = obj.total_price
            if total is None:
                return "$0.00"
            price = float(total)
            return f"${price:.2f}"
        except (ValueError, TypeError, AttributeError):
            return "$0.00"

    total_price_display.short_description = "Total Price"

    def order_status(self, obj):
        """Display order status."""
        return obj.order.get_status_display()

    order_status.short_description = "Order Status"

    def calculated_total_price(self, obj):
        """Display calculated total price in admin form."""
        if obj and hasattr(obj, "total_price") and obj.total_price:
            try:
                price = float(obj.total_price)
                return f"${price:.2f}"
            except (ValueError, TypeError):
                return "-"
        return "-"

    calculated_total_price.short_description = "Total Price"


@admin.register(get_user_model(), site=portal_site)
class UserAdmin(BaseUserAdmin):
    pass
