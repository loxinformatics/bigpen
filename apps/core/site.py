from django.contrib.admin import AdminSite as DjangoAdminSite

from .views import signin, signout


class AdminSite(DjangoAdminSite):
    """
    Custom admin site for the organization.

    Overrides default admin login/logout URLs with custom views
    for authentication that may include branding, layout, or behavior
    tailored to the organization.
    """

    site_header = "Portal Manager"  # Appears at the top of each admin page
    site_title = "Management Portal"  # Appears in the <title> of admin pages
    index_title = "Welcome to the Portal Manager"  # Appears on the admin homepage

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
