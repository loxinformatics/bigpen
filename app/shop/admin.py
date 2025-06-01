from django.contrib import admin

from .models import Category, Item, ItemImage, Order, OrderItem


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1  # Number of empty image fields shown by default


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_filter = ("category",)
    inlines = [ItemImageInline]
    readonly_fields = ("calculated_current_price", "calculated_discount_percentage")

    def calculated_current_price(self, obj):
        if not obj or obj.current_price is None:
            return "-"
        return f"{obj.current_price:.2f}"

    def calculated_discount_percentage(self, obj):
        if not obj or obj.discount_percentage is None:
            return "-"
        return f"-{obj.discount_percentage:.0f}%"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "fulfilled")
    inlines = [OrderItemInline]
