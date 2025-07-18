from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .stock import Item


class Order(models.Model):
    """Order model with staff assignment functionality."""

    ORDER_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="orders",
        help_text="Customer who placed the order",
    )
    assigned_to = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_orders",
        help_text="Staff member assigned to work on this order",
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default="pending",
        help_text="Current status of the order",
    )
    assigned_at = models.DateTimeField(
        null=True, blank=True, help_text="When the order was assigned to staff"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)
    notes = models.TextField(blank=True, help_text="Internal notes about the order")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - {self.get_status_display()}"

    def clean(self):
        """Validate order assignment."""
        if self.assigned_to and not self.assigned_to.is_staff:
            raise ValidationError("Only staff members can be assigned to orders")

    def assign_to_staff(self, staff_user):
        """Assign order to a staff member and set status to in_progress."""
        if not staff_user.is_staff:
            raise ValidationError("Only staff members can be assigned to orders")

        if self.assigned_to is not None:
            raise ValidationError("Order is already assigned to someone else")

        self.assigned_to = staff_user
        self.status = "in_progress"
        self.assigned_at = timezone.now()
        self.save()

    def unassign_order(self):
        """Remove assignment from order."""
        self.assigned_to = None
        self.status = "pending"
        self.assigned_at = None
        self.save()

    def can_be_assigned_to(self, staff_user):
        """Check if order can be assigned to a specific staff member."""
        return (
            staff_user.is_staff
            and self.assigned_to is None
            and self.status == "pending"
        )

    @property
    def is_available_for_assignment(self):
        """Check if order is available for staff to pick up."""
        return self.assigned_to is None and self.status == "pending"

    def get_total_items(self):
        """Get total number of items in the order."""
        return sum(item.quantity for item in self.order_items.all())

    def get_total_price(self):
        """Calculate total price of the order."""
        total = 0
        for order_item in self.order_items.all():
            if order_item.item.current_price:
                total += order_item.item.current_price * order_item.quantity
        return total


class OrderItem(models.Model):
    """Individual items within an order."""

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, help_text="The item being ordered"
    )
    quantity = models.PositiveIntegerField(
        default=1, help_text="Quantity of this item in the order"
    )
    price_at_time = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Price of the item when the order was placed (for historical accuracy)",
    )

    class Meta:
        unique_together = ["order", "item"]

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    def save(self, *args, **kwargs):
        """Save the current price when creating the order item."""
        if not self.price_at_time and self.item.current_price:
            self.price_at_time = self.item.current_price
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        """Get total price for this order item."""
        price = self.price_at_time or self.item.current_price or 0
        return price * self.quantity
        return price * self.quantity
