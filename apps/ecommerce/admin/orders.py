from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import path
from django.utils import timezone
from django.utils.html import format_html
from django.views.decorators.http import require_http_methods

from apps.core.admin import admin_site

from ..models.orders import Order, OrderItem


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


@admin.register(Order, site=admin_site)
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


@admin.register(OrderItem, site=admin_site)
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
