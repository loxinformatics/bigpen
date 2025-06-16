from django.contrib.auth import get_user_model
from django.db import models

from apps.core.models import User


class CustomUser(User):
    pass


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    image = models.ImageField(
        upload_to="shop/categories/",
        blank=True,
        null=True,
        help_text="Optional. Image representing the category.",
    )
    bootstrap_icon = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional. Bootstrap icon class or path for the category. Example: 'bi bi-cart' for a shopping cart icon. Find icons at [Bootstrap Icons](https://icons.getbootstrap.com/).",
    )
    name = models.CharField(max_length=255, help_text="Name of the category.")
    description = models.TextField(
        blank=True, help_text="Optional. Description of the category."
    )

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items",
        help_text="Category this item belongs to.",
    )
    name = models.CharField(max_length=255, help_text="Name of the item.")
    image = models.ImageField(
        upload_to="shop/items/",
        help_text="Main image for the item.",
        default="/shop/items/default_item_image.jpg",
    )
    bootstrap_icon = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional. Bootstrap icon class or path for the item. Example: 'bi bi-cart' for a shopping cart icon. Find icons at [Bootstrap Icons](https://icons.getbootstrap.com/).",
    )
    description = models.TextField(
        blank=True,
        help_text="Optional. Detailed description of the item.",
    )
    quantity = models.PositiveIntegerField(
        default=0,
        help_text="Available quantity in stock.",
    )
    is_featured = models.BooleanField(default=False, help_text="Mark as featured item.")
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
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Date and time when the item was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the item was last updated.",
    )

    def __str__(self):
        return self.name

    @property
    def current_price(self):
        if self.original_price is None or self.discount is None:
            return None
        return self.original_price - self.discount

    @property
    def discount_percentage(self):
        """
        Returns the discount as a negative percentage string (e.g., -40 for 40% off).
        """
        if not self.original_price or self.original_price == 0:
            return 0
        return -(self.discount / self.original_price * 100)


class ItemImage(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="otherImages",
        help_text="Item this image belongs to.",
    )
    image = models.ImageField(upload_to="shop/items/", help_text="Image for the item.")


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
