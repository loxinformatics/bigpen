# from django.contrib.auth.models import Permission
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import models
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import path
from django.utils import timezone
from django.utils.html import format_html
from django.views.decorators.http import require_http_methods

from apps.core.site import portal_site
from apps.home.forms import UserChangeForm
from apps.home.models import Category, Item, ItemImage, Order, OrderItem

# ============================================================================
# AUTH ADMIN
# ============================================================================


@admin.register(Group, site=portal_site)
class GroupAdmin(BaseGroupAdmin):
    pass


@admin.register(get_user_model(), site=portal_site)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm

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


# ============================================================================
# STOCK ADMIN
# ============================================================================


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


# ============================================================================
# ORDER ADMIN
# ============================================================================


class OrderStatusFilter(admin.SimpleListFilter):
    """Custom filter for order status."""

    title = "order status"
    parameter_name = "order_status"

    def lookups(self, request, model_admin):
        return (
            ("pending", "Pending"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
            ("unassigned", "Unassigned Orders"),
            ("my_orders", "My Assigned Orders"),  # New filter
        )

    def queryset(self, request, queryset):
        if self.value() == "unassigned":
            return queryset.filter(assigned_to__isnull=True, status="pending")
        elif self.value() == "my_orders":
            return queryset.filter(assigned_to=request.user)
        elif self.value():
            return queryset.filter(status=self.value())
        return queryset


class StaffOrderFilter(admin.SimpleListFilter):
    """Filter orders by staff assignment."""

    title = "staff assignment"
    parameter_name = "staff_filter"

    def lookups(self, request, model_admin):
        # Get all staff members who have orders assigned
        User = get_user_model()
        staff_with_orders = (
            User.objects.filter(assigned_orders__isnull=False)
            .distinct()
            .values_list("id", "username")
        )

        lookups = [
            ("my_orders", "My Orders"),
            ("unassigned", "Unassigned"),
        ]

        for staff_id, username in staff_with_orders:
            lookups.append((f"staff_{staff_id}", f"{username}'s Orders"))

        return lookups

    def queryset(self, request, queryset):
        if self.value() == "my_orders":
            return queryset.filter(assigned_to=request.user)
        elif self.value() == "unassigned":
            return queryset.filter(assigned_to__isnull=True)
        elif self.value() and self.value().startswith("staff_"):
            staff_id = self.value().replace("staff_", "")
            return queryset.filter(assigned_to_id=staff_id)
        return queryset


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
                price = float(obj.total_price)
                return f"${price:.2f}"
            except (ValueError, TypeError):
                return "-"
        return "-"

    total_price_display.short_description = "Total Price"


@admin.register(Order, site=portal_site)
class OrderAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Order model with staff-specific functionality.
    """

    list_display = (
        "id",
        "user",
        "status_display",
        "assigned_to_display",
        "total_items_display",
        "total_price_display",
        "created_at",
        "priority_indicator",
        "fulfilled",  # Make sure fulfilled is here
    )
    list_editable = ("fulfilled",)
    list_filter = (
        StaffOrderFilter,  # New enhanced filter
        OrderStatusFilter,
        "fulfilled",
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

    actions = [
        "assign_to_me",
        "unassign_orders",
        "mark_completed",
        "mark_in_progress",
        "quick_assign_multiple",  # New action
    ]

    def get_queryset(self, request):
        """Optimize queryset and filter for staff members."""
        qs = super().get_queryset(request).select_related("user", "assigned_to")

        # If user is staff but not superuser, show only their orders and unassigned orders
        if not request.user.is_superuser and request.user.is_staff:
            # Show orders assigned to them + unassigned orders they can pick up
            qs = qs.filter(
                models.Q(assigned_to=request.user)
                | models.Q(assigned_to__isnull=True, status="pending")
            )

        return qs

    def get_urls(self):
        """Add custom URLs for staff dashboard."""
        urls = super().get_urls()
        custom_urls = [
            path(
                "staff-dashboard/",
                self.admin_site.admin_view(self.staff_dashboard_view),
                name="order_staff_dashboard",
            ),
            path(
                "quick-assign/<int:order_id>/",
                self.admin_site.admin_view(self.quick_assign_view),
                name="order_quick_assign",
            ),
        ]
        return custom_urls + urls

    def staff_dashboard_view(self, request):
        """Custom dashboard view for staff members."""
        if not request.user.is_staff:
            messages.error(request, "Access denied. Staff members only.")
            return redirect("admin:index")

        # Get staff member's assigned orders (now in_progress)
        my_orders = Order.objects.filter(assigned_to=request.user).select_related(
            "user"
        )

        # Get available orders for assignment
        available_orders = Order.objects.filter(
            assigned_to__isnull=True, status="pending"
        ).select_related("user")

        # Get summary statistics
        stats = {
            "my_pending": my_orders.filter(status="in_progress").count(),
            "my_completed_today": my_orders.filter(
                status="completed", assigned_at__date=timezone.now().date()
            ).count(),
            "available_orders": available_orders.count(),
        }

        context = {
            "title": "Staff Order Dashboard",
            "my_orders": my_orders[:10],
            "available_orders": available_orders[:10],
            "stats": stats,
            "opts": self.model._meta,
        }

        return render(request, "admin/order_staff_dashboard.html", context)

    @require_http_methods(["POST"])
    def quick_assign_view(self, request, order_id):
        """Quick assign order via AJAX."""
        try:
            order = Order.objects.get(id=order_id)
            if order.can_be_assigned_to(request.user):
                order.assign_to_staff(request.user)
                return JsonResponse(
                    {
                        "success": True,
                        "message": f"Order #{order_id} assigned to you successfully.",
                    }
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "message": f"Order #{order_id} cannot be assigned.",
                    }
                )
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "message": "Order not found."})
        except ValidationError as e:
            return JsonResponse({"success": False, "message": str(e)})

    def changelist_view(self, request, extra_context=None):
        """Add extra context for staff members."""
        extra_context = extra_context or {}

        if request.user.is_staff:
            # Add quick stats for staff
            my_orders_count = Order.objects.filter(assigned_to=request.user).count()
            available_count = Order.objects.filter(
                assigned_to__isnull=True, status="pending"
            ).count()

            extra_context.update(
                {
                    "my_orders_count": my_orders_count,
                    "available_orders_count": available_count,
                    "show_staff_dashboard_link": True,
                }
            )

        return super().changelist_view(request, extra_context=extra_context)

    # Enhanced display methods
    def status_display(self, obj):
        """Display order status with color coding."""
        status_colors = {
            "pending": "#ffc107",
            "in_progress": "#007bff",
            "completed": "#28a745",
            "cancelled": "#dc3545",
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
        return format_html('<span style="color: #dc3545;">🔄 Available</span>')

    assigned_to_display.short_description = "Assigned To"

    def priority_indicator(self, obj):
        """Show priority indicator for urgent orders."""
        from datetime import timedelta

        from django.utils import timezone

        # Mark orders older than 24 hours as urgent
        if obj.created_at < timezone.now() - timedelta(hours=24):
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">🔥 Urgent</span>'
            )
        return format_html('<span style="color: #28a745;">✓ Normal</span>')

    priority_indicator.short_description = "Priority"

    def fulfillment_status(self, obj):
        """Show fulfillment status."""
        if obj.fulfilled:
            return format_html('<span style="color: #28a745;">✅ Fulfilled</span>')
        return format_html('<span style="color: #ffc107;">⏳ Pending</span>')

    fulfillment_status.short_description = "Fulfillment"

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
            price = float(total)
            return f"${price:.2f}"
        except (ValueError, TypeError, AttributeError):
            return "$0.00"

    total_price_display.short_description = "Total Price"

    # Enhanced actions
    def assign_to_me(self, request, queryset):
        """Action to assign selected orders to the current user."""
        if not request.user.is_staff:
            self.message_user(
                request, "Only staff members can be assigned orders.", level="ERROR"
            )
            return

        assigned_count = 0
        errors = []

        for order in queryset:
            if order.can_be_assigned_to(request.user):
                try:
                    order.assign_to_staff(request.user)
                    assigned_count += 1
                except ValidationError as e:
                    errors.append(f"Order {order.id}: {e}")

        if assigned_count:
            self.message_user(
                request, f"Successfully assigned {assigned_count} orders to you."
            )

        if errors:
            for error in errors:
                self.message_user(request, error, level="ERROR")

        if not assigned_count and not errors:
            self.message_user(request, "No orders could be assigned.", level="WARNING")

    assign_to_me.short_description = (
        "Assign selected orders to me (moves to In Progress)"
    )

    def quick_assign_multiple(self, request, queryset):
        """Quickly assign multiple unassigned orders to current user."""
        if not request.user.is_staff:
            self.message_user(
                request, "Only staff members can assign orders.", level="ERROR"
            )
            return

        unassigned_orders = queryset.filter(assigned_to__isnull=True, status="pending")
        assigned_count = 0

        for order in unassigned_orders:
            try:
                order.assign_to_staff(request.user)
                assigned_count += 1
            except ValidationError:
                continue

        if assigned_count:
            self.message_user(
                request, f"Quick assigned {assigned_count} unassigned orders to you."
            )
        else:
            self.message_user(
                request, "No unassigned orders found in selection.", level="WARNING"
            )

    quick_assign_multiple.short_description = (
        "Quick assign unassigned orders to me (moves to In Progress)"
    )

    def mark_in_progress(self, request, queryset):
        """Action to mark selected orders as in progress."""
        updated = queryset.update(status="in_progress")
        self.message_user(
            request, f"Successfully marked {updated} orders as in progress."
        )

    mark_in_progress.short_description = "Mark selected orders as in progress"

    # Form customization
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter assigned_to field to only show staff_admin users."""
        if db_field.name == "assigned_to":
            User = get_user_model()
            # Only users who have the staff_admin role
            kwargs["queryset"] = User.objects.filter(
                groups__name="staff_admin"
            ).distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Summary methods (keeping your existing ones)
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

            price = float(total)
            return f"Total: ${price:.2f} ({item_count} items)"
        except (ValueError, TypeError, AttributeError):
            return "Total: $0.00 (0 items)"

    total_price_summary.short_description = "Price Summary"


@admin.register(OrderItem, site=portal_site)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderItem model with pricing and inventory details."""

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


# Register Item with the default admin site for autocomplete support
# @admin.register(Item)
# class DefaultItemAdmin(admin.ModelAdmin):
#     search_fields = ("name", "description")
