from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseUser, BootstrapIcon, DateFields, Ordering


class Category(Ordering, BootstrapIcon, DateFields):
    """Category model for organizing shop items."""

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["order", "name"]

    image = models.ImageField(
        upload_to="shop/categories/",
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
        upload_to="shop/items/",
        help_text="Main image for the item.",
        default="/shop/items/default_item_image.jpg",
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
        upload_to="shop/items/", help_text="Additional image for the item."
    )
    alt_text = models.CharField(
        max_length=255, blank=True, help_text="Alternative text for accessibility."
    )
    is_active = models.BooleanField(
        default=True, help_text="Whether this image should be displayed."
    )

    def __str__(self):
        return f"{self.item.name} - Image {self.id}"


class User(BaseUser):
    # profile_image = models.ImageField(blank=True, null=True, upload_to="core/user")
    # title = models.CharField(max_length=255, blank=True)
    pass


# class Order(models.Model):
#     user = models.ForeignKey(
#         get_user_model(), on_delete=models.CASCADE, related_name="orders"
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     fulfilled = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Order #{self.id} by {self.user.username}"


# class OrderItem(models.Model):
#     order = models.ForeignKey(
#         Order, on_delete=models.CASCADE, related_name="order_items"
#     )
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.quantity} x {self.item.name}"
