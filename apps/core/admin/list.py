from django.contrib import admin

from ..models.list import ListCategory, ListItem
from .site import admin_site


@admin.register(ListCategory, site=admin_site)
class ListCategoryAdmin(admin.ModelAdmin):
    """
    Admin for ListCategory model. Allow permissions only for superusers.
    """

    list_display = (
        "name",
        "bootstrap_icon",
        "order",
    )
    list_editable = ("order",)
    ordering = ("order",)
    search_fields = ("name",)
    fieldsets = (
        ("Category Details", {"fields": ("name",)}),
        ("Display Options", {"fields": ("bootstrap_icon", "order")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")


# Custom filter for ListItem based on category name
class CategoryNameFilter(admin.SimpleListFilter):
    title = "Category"
    parameter_name = "category_name"

    def lookups(self, request, model_admin):
        categories = set(ListCategory.objects.values_list("name", flat=True))
        return [(cat, cat) for cat in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__name=self.value())
        return queryset


@admin.register(ListItem, site=admin_site)
class ListItemAdmin(admin.ModelAdmin):
    """
    Admin for ListItem model with enhanced display, filtering,
    search, and form behavior.
    """

    list_display = (
        "name",
        "bootstrap_icon",
        "category",
        "order",
    )
    list_editable = (
        "bootstrap_icon",
        "order",
    )
    list_filter = (CategoryNameFilter, "category")
    search_fields = ("name", "description")
    ordering = ("order", "name")
    fieldsets = (
        ("Item Details", {"fields": ("name", "description", "category")}),
        ("Display Options", {"fields": ("bootstrap_icon", "order")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    readonly_fields = ("created_at", "updated_at")

    def get_form(self, request, obj=None, **kwargs):
        """
        Remove '+' add-related button from the category field.
        """
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["category"].widget.can_add_related = False
        return form
