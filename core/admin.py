from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from .models import CoreProvider, ListCategory, ListItem


class BaseSingletonAdmin(admin.ModelAdmin):
    """
    Base admin class to enforce singleton behavior in the Django admin interface.
    """

    def changelist_view(self, request, extra_context=None):
        opts = self.model._meta
        if self.model.objects.exists():
            # Redirect to the change view for the singleton instance
            singleton_instance = self.model.objects.first()
            return HttpResponseRedirect(
                reverse(
                    "admin:%s_%s_change" % (opts.app_label, opts.model_name),
                    args=[singleton_instance.pk],
                )
            )
        else:
            # Redirect to the add view if no instance exists
            return HttpResponseRedirect(
                reverse("admin:%s_%s_add" % (opts.app_label, opts.model_name))
            )

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        # Hide 'save and add another' button
        extra_context["show_save_and_add_another"] = False
        return super(BaseSingletonAdmin, self).changeform_view(
            request, object_id, form_url, extra_context=extra_context
        )


@admin.register(CoreProvider)
class CoreProviderAdmin(BaseSingletonAdmin):
    def get_fieldsets(self, request, obj=None):
        """Customize fieldsets based on user permissions with collapsible sections."""
        fieldsets = [
            (
                "Company Info",
                {"fields": ("name", "short_name", "motto")},
            ),  # Always visible
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
                    "classes": ("collapse",),  # Collapsible
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
                    "classes": ("collapse",),  # Collapsible
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
                    "classes": ("collapse",),  # Collapsible
                },
            ),
            (
                "Branding & Icons",
                {
                    "fields": ("logo", "favicon", "apple_touch_icon"),
                    "classes": ("collapse",),  # Collapsible
                },
            ),
        ]
        return fieldsets


@admin.register(ListCategory)
class ListCategoryAdmin(admin.ModelAdmin):
    pass


class CategoryNameFilter(SimpleListFilter):
    title = "Category"
    parameter_name = "category_name"

    def lookups(self, request, model_admin):
        categories = set(ListCategory.objects.values_list("name", flat=True))
        return [(cat, cat) for cat in categories]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__name=self.value())
        return queryset


@admin.register(ListItem)
class ListItemAdmin(admin.ModelAdmin):
    list_filter = (CategoryNameFilter,)

    def get_form(self, request, obj=None, **kwargs):
        # Customize the form to remove the add button for the 'groups' field.
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["category"].widget.can_add_related = False
        return form
