from django.conf import settings
from django.contrib.admin import AdminSite as DjangoAdminSite
from django.utils.translation import gettext_lazy as _

from ..views.auth import signin, signout


class AdminSite(DjangoAdminSite):
    """
    Custom admin site for the organization.

    Overrides default admin login/logout URLs with custom views
    for authentication that may include branding, layout, or behavior
    tailored to the organization.
    """

    SITE_NAME = settings.SITE_NAME

    site_header = _("{} Administration").format(SITE_NAME)
    site_title = _("{} Admin").format(SITE_NAME)
    index_title = _("Welcome to {} Portal Manager").format(SITE_NAME)

    def get_urls(self):
        """
        Returns a list of URL patterns for the custom admin site.

        Adds custom login and logout paths (handled by `signin` and `signout` views),
        and appends the default admin site URLs.
        """
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path("login/", signin, name="admin_login"),
            path("logout/", signout, name="admin_logout"),
        ]
        return custom_urls + urls


# Create custom admin site instance
admin_site = AdminSite(name="admin_site")
