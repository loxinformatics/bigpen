import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.home"

    def ready(self):
        try:
            from apps.core.config.navigation import nav_config
            from apps.core.config.urls import urls_config

            # Configure landing url
            urls_config.register_landing_url("landing", self.name)

            # nav items
            nav_config.register(
                name="Home",
                url_name="landing",
                fragment="hero",
                order=0,
                icon="bi bi-house",
            )
            nav_config.register(
                name="Contact",
                url_name="landing",
                fragment="contact",
                order=3,
                icon="bi bi-envelope",
            )
            # nav_config.register(
            #     name="Account",
            #     dropdown_items=[
            #         {
            #             "name": "Login",
            #             "url_name": "login",
            #             "icon": "bi bi-box-arrow-in-right",
            #         },
            #         {
            #             "name": "Sign Up",
            #             "url_name": "signup",
            #             "icon": "bi bi-person-plus",
            #         },
            #     ],
            #     order=1,
            #     icon="bi bi-person",
            #     requires_auth=False,
            # )
            # nav_config.register(
            #     name="Profile",
            #     dropdown_items=[
            #         {
            #             "name": "Dashboard",
            #             "url_name": "dashboard",
            #             "icon": "bi bi-speedometer2",
            #         },
            #         {"name": "Portal", "url_name": "portal", "icon": "bi bi-door-open"},
            #         {"name": "Settings", "url_name": "settings", "icon": "bi bi-gear"},
            #         {
            #             "name": "Logout",
            #             "url_name": "logout",
            #             "icon": "bi bi-box-arrow-right",
            #         },
            #     ],
            #     order=1,
            #     icon="bi bi-person-circle",
            #     requires_auth=True,
            # )

            # # Alternative method: Register dropdown parent then add children
            # # This is useful if you want to conditionally add dropdown items
            # """
            # # Create auth dropdown
            # nav_config.register_dropdown(
            #     name="Account",
            #     icon="bi bi-person",
            #     order=1,
            #     requires_auth=False
            # )
            # nav_config.add_dropdown_item("Account", "Login", "login", icon="bi bi-box-arrow-in-right")
            # nav_config.add_dropdown_item("Account", "Sign Up", "signup", icon="bi bi-person-plus")

            # # Create profile dropdown
            # nav_config.register_dropdown(
            #     name="Profile",
            #     icon="bi bi-person-circle",
            #     order=1,
            #     requires_auth=True
            # )
            # nav_config.add_dropdown_item("Profile", "Dashboard", "dashboard", icon="bi bi-speedometer2")
            # nav_config.add_dropdown_item("Profile", "Portal", "portal", icon="bi bi-door-open")
            # """

        except Exception as e:
            logger.warning(f"Failed to configure core app settings: {e}")
