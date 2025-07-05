from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.core.models import BootstrapIcon, DateFields, Ordering

# ============================================================================
# AUTH MODELS
# ============================================================================


class User(AbstractUser, Ordering):
    """Custom User model with group-based permissions and staff status management"""

    # 👇make email optional
    email = models.EmailField(blank=True, null=True)
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "auth_user"
        ordering = ["order", "username"]

    def clean(self):
        """Validate group assignments according to business rules"""
        super().clean()

        # Get group names from the many-to-many field
        if self.pk:  # Only check if user exists (has been saved)
            group_names = set(self.groups.values_list("name", flat=True))
            self._validate_group_combinations(group_names)

    def _validate_group_combinations(self, group_names):
        """Validate that group combinations follow business rules"""
        exclusive_groups = {"standard", "manager", "superuser"}
        staff_groups = {"normal_staff", "blogger_staff"}

        # Check for exclusive groups
        exclusive_found = group_names.intersection(exclusive_groups)
        if len(exclusive_found) > 1:
            raise ValidationError(
                f"User can only belong to one of these groups: {', '.join(exclusive_groups)}. "
                f"Found: {', '.join(exclusive_found)}"
            )

        # Check if exclusive group is mixed with others
        if exclusive_found:
            exclusive_group = list(exclusive_found)[0]
            other_groups = group_names - {exclusive_group}
            if other_groups:
                raise ValidationError(
                    f"'{exclusive_group}' group cannot be combined with other groups. "
                    f"Found additional groups: {', '.join(other_groups)}"
                )

        # If no exclusive groups, ensure only staff groups are present
        elif group_names:
            invalid_combinations = group_names - staff_groups
            if invalid_combinations:
                raise ValidationError(
                    f"Invalid group combination. When not using exclusive groups "
                    f"(standard, manager, superuser), only staff groups are allowed: "
                    f"{', '.join(staff_groups)}. Found invalid: {', '.join(invalid_combinations)}"
                )

    def save(self, *args, **kwargs):
        """Custom save method to handle default group assignment and staff status"""
        is_new_user = self.pk is None

        # Set default values for new users
        if is_new_user:
            if self.is_superuser:
                # Superusers get superuser group by default
                self.is_staff = True
            else:
                # Regular users get standard group by default
                self.is_staff = False

        # Call the parent save method first
        super().save(*args, **kwargs)

        # Handle group assignment for new users
        if is_new_user:
            if self.is_superuser:
                superuser_group, created = Group.objects.get_or_create(name="superuser")
                self.groups.set([superuser_group])
            else:
                standard_group, created = Group.objects.get_or_create(name="standard")
                self.groups.set([standard_group])

    def update_staff_status(self):
        """Update is_staff based on group membership"""
        group_names = set(self.groups.values_list("name", flat=True))

        # Only 'standard' group users should have is_staff = False
        if group_names == {"standard"}:
            self.is_staff = False
        else:
            # All other groups should have is_staff = True
            self.is_staff = True

        # Save without triggering the full save logic again
        super().save(update_fields=["is_staff"])


@receiver(post_save, sender=User)
def update_user_staff_status(sender, instance, **kwargs):
    """Signal to update staff status when user groups change"""
    if not kwargs.get("raw", False):  # Don't run during fixtures loading
        # Use a flag to prevent infinite recursion
        if not hasattr(instance, "_updating_staff_status"):
            instance._updating_staff_status = True
            try:
                instance.update_staff_status()
            finally:
                delattr(instance, "_updating_staff_status")


# ============================================================================
# STOCK MODELS
# ============================================================================


class Category(Ordering, BootstrapIcon, DateFields):
    """Category model for organizing shop items."""

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order", "name"]

    image = models.ImageField(
        upload_to="portfolio/categories/",
        blank=True,
        null=True,
        help_text="Optional. Image representing the category.",
    )
    name = models.CharField(max_length=255, help_text="Name of the category.")
    description = models.TextField(
        blank=True, help_text="Optional. Description of the category."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this category is active and visible to customers.",
    )

    def __str__(self):
        return self.name

    def get_active_items(self):
        """Return only active items in this category."""
        return self.items.filter(is_active=True)


class Item(Ordering, BootstrapIcon, DateFields):
    """Main item model with enhanced inventory and pricing features."""

    class Meta:
        ordering = ["order", "name"]

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items",
        help_text="Category this item belongs to.",
    )
    name = models.CharField(max_length=255, help_text="Name of the item.")
    main_image = models.ImageField(
        upload_to="portfolio/items/",
        help_text="Main image for the item.",
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        help_text="Optional. Detailed description of the item.",
    )

    # Inventory management
    quantity = models.PositiveIntegerField(
        default=0,
        help_text="Total quantity in stock.",
    )
    reserved_quantity = models.PositiveIntegerField(
        default=0,
        help_text="Quantity reserved for pending orders.",
    )
    low_stock_threshold = models.PositiveIntegerField(
        default=5,
        help_text="Alert when stock falls below this number.",
    )

    # Order constraints
    min_order_quantity = models.PositiveIntegerField(
        default=1,
        help_text="Minimum quantity that can be ordered at once.",
    )
    max_order_quantity = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum quantity that can be ordered at once (optional).",
    )

    # Status
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this item is active and available for purchase.",
    )
    is_featured = models.BooleanField(default=False, help_text="Mark as featured item.")

    # Pricing
    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Original price of the item.",
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text="Optional. Discount amount to subtract from the original price.",
    )

    def __str__(self):
        return self.name

    def clean(self):
        if (
            self.max_order_quantity
            and self.min_order_quantity > self.max_order_quantity
        ):
            raise ValidationError(
                "Minimum order quantity cannot exceed maximum order quantity."
            )

    @property
    def available_quantity(self):
        """Get quantity available for new orders."""
        return max(0, self.quantity - self.reserved_quantity)

    @property
    def is_in_stock(self):
        """Check if item has available stock."""
        return self.available_quantity > 0

    @property
    def is_low_stock(self):
        """Check if item is running low on stock."""
        return self.available_quantity <= self.low_stock_threshold

    @property
    def current_price(self):
        """Get current price with discount applied."""
        if self.original_price is None or self.discount is None:
            return None
        return self.original_price - self.discount

    @property
    def discount_percentage(self):
        """Returns the discount as a negative percentage."""
        if not self.original_price or self.original_price == 0:
            return 0
        return -(self.discount / self.original_price * 100)

    def reserve_stock(self, quantity):
        """Reserve stock for an order. Returns True if successful."""
        if quantity <= self.available_quantity:
            self.reserved_quantity += quantity
            self.save(update_fields=["reserved_quantity"])
            return True
        return False

    def release_stock(self, quantity):
        """Release reserved stock (e.g., when order is cancelled)."""
        self.reserved_quantity = max(0, self.reserved_quantity - quantity)
        self.save(update_fields=["reserved_quantity"])

    def consume_stock(self, quantity):
        """Consume stock when order is completed."""
        if quantity <= self.quantity:
            self.quantity -= quantity
            self.reserved_quantity = max(0, self.reserved_quantity - quantity)
            self.save(update_fields=["quantity", "reserved_quantity"])
            return True
        return False


class ItemImage(DateFields):
    """Additional images for items."""

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="other_images",
        help_text="Item this image belongs to.",
    )
    image = models.ImageField(
        upload_to="portfolio/items/other_images/",
        help_text="Additional image for the item.",
    )
    alt_text = models.CharField(
        max_length=255, blank=True, help_text="Alternative text for accessibility."
    )
    is_active = models.BooleanField(
        default=True, help_text="Whether this image should be displayed."
    )

    def __str__(self):
        return f"{self.item.name} - Image {self.id}"


# ============================================================================
# ORDER MODELS
# ============================================================================


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
