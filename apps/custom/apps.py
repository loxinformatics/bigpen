import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class CustomConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.custom"
    verbose_name = "Functional Modules"

    def ready(self):
        try:
            from apps.core.config.urls import urls_config
            from apps.core.config.auth import auth_config
            from apps.core.config.navigation import nav_config

            # Disable auth pages
            # auth_config.disable_page("signup")
            # auth_config.disable_page("signin")

            # Configure page settings (no role management needed)
            auth_config.configure_username_field(
                label="Phone Number",
                placeholder="Enter your Phone Number (with country code e.g. +254700000000)",
            )

            # nav items
            nav_config.register(
                name="Dashboard",
                url_name="custom:dashboard",
                order=4,
                icon="bi bi-shop",
                auth_status="private",
            )
            nav_config.register(
                name="Contact",
                url_name="custom:contact",
                order=4,
                icon="bi bi-envelope",
                auth_status="private",
            )

            # Register dashboard as login redirect URL
            urls_config.register_login_redirect_url("custom:dashboard", self.name)

            logger.info("custom app configured successfully")

        except Exception as e:
            logger.warning(f"Failed to configure custom app config: {e}")
