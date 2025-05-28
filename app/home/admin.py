from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from .models import ListCategory, ListItem, Organization

# admin.site.site_header = settings.ORG_FULLNAME
# admin.site.site_title = f"Admin | {settings.ORG_SHORTNAME if settings.ORG_SHORTNAME else settings.ORG_FULLNAME}"
# admin.site.index_title = f"{settings.ORG_FULLNAME} Administration"


class BaseSingletonAdmin(admin.ModelAdmin):
    """
    Base admin class that enforces singleton behavior in the admin interface.
    Only one instance of the model can exist, and users are automatically
    redirected to edit the existing instance instead of seeing a changelist.
    """

    def changelist_view(self, request, extra_context=None):
        opts = self.model._meta
        if self.model.objects.exists():
            # Redirect to the change view for the single existing instance
            singleton_instance = self.model.objects.first()
            return HttpResponseRedirect(
                reverse(
                    "admin:%s_%s_change" % (opts.app_label, opts.model_name),
                    args=[singleton_instance.pk],
                )
            )
        else:
            # No instance exists; redirect to the add view
            return HttpResponseRedirect(
                reverse("admin:%s_%s_add" % (opts.app_label, opts.model_name))
            )

    def has_add_permission(self, request):
        # Prevent adding more than one instance
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the singleton instance
        return False

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        # Hide 'save and add another' button in the form
        extra_context["show_save_and_add_another"] = False
        return super().changeform_view(
            request, object_id, form_url, extra_context=extra_context
        )


@admin.register(Organization)
class OrganizationAdmin(BaseSingletonAdmin):
    def get_fieldsets(self, request, obj=None):
        """
        Organize CoreProvider fields into collapsible sections in the admin form.
        """
        fieldsets = [
            (
                "Logo & Icons",
                {
                    "fields": ("logo", "favicon", "apple_touch_icon"),
                },
            ),
            (
                "Contact Info",
                {
                    "fields": (
                        "website",
                        "primary_phone",
                        "secondary_phone",
                        "other_phone",
                        "primary_email",
                        "secondary_email",
                        "other_email",
                    ),
                },
            ),
            (
                "Addressing Info",
                {
                    "fields": (
                        "building",
                        "street",
                        "PO_box",
                        "city_name",
                        "zip_code",
                        "map_url",
                    ),
                },
            ),
            (
                "Social Media",
                {
                    "fields": (
                        "facebook",
                        "twitter",
                        "instagram",
                        "linkedin",
                        "tiktok",
                        "youtube",
                        "whatsapp",
                        "telegram",
                        "snapchat",
                        "pinterest",
                    ),
                },
            ),
        ]
        return fieldsets


@admin.register(ListCategory)
class ListCategoryAdmin(admin.ModelAdmin):
    """
    Admin for ListCategory model, restricted to superusers only.
    Hides the model from the admin index and disallows access for non-superusers.
    """

    def has_module_permission(self, request):
        # Hide from the admin sidebar for non-superusers
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        # Prevent viewing or accessing the model directly for non-superusers
        return request.user.is_superuser


class CategoryNameFilter(SimpleListFilter):
    """
    Custom filter to filter ListItems based on the name of their category.
    """

    title = "Category"  # Displayed label for the filter in admin
    parameter_name = "category_name"

    def lookups(self, request, model_admin):
        # Provide a list of (value, label) tuples for the filter
        categories = set(ListCategory.objects.values_list("name", flat=True))
        return [(cat, cat) for cat in categories]

    def queryset(self, request, queryset):
        # Apply the filter to the queryset
        if self.value():
            return queryset.filter(category__name=self.value())
        return queryset


@admin.register(ListItem)
class ListItemAdmin(admin.ModelAdmin):
    """
    Admin for ListItem model with category filtering and no 'add related' button.
    """

    list_filter = (CategoryNameFilter,)  # Use custom filter

    def get_form(self, request, obj=None, **kwargs):
        """
        Customize form to remove the '+' (add related) button next to the category field.
        """
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["category"].widget.can_add_related = False
        return form
