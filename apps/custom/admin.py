from django.contrib import admin
from django.contrib.auth import get_user_model

from apps.core.admin import BaseUserAdmin
from apps.core.admin_site import portal_site

from .models import Category, Item, ItemImage, Order, OrderItem


@admin.register(get_user_model(), site=portal_site)
class UserAdmin(BaseUserAdmin):
    pass


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1  # Number of empty image fields shown by default


@admin.register(Item, site=portal_site)
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


@admin.register(Category, site=portal_site)
class CategoryAdmin(admin.ModelAdmin):
    pass


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order, site=portal_site)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "fulfilled")
    inlines = [OrderItemInline]
