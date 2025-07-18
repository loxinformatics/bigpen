import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)

APP_NAME = "apps.blog"


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = APP_NAME

    def ready(self):
        try:
            from apps.core.management.config.navigation import nav_config

            # nav items
            nav_config.register(
                name="Blog",
                url_name="blogpage",
                order=4,
                icon="bi bi-journal-text",
            )

            logger.info(f"{self.name} configured successfully")

        except Exception as e:
            logger.warning(f"Failed to configure {self.name} config: {e}")
