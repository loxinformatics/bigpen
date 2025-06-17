import logging

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse

logger = logging.getLogger(__name__)


class URLsConfig:
    """
    Registry for managing landing URL across Django apps.
    Allows apps to register themselves as the landing URL provider.
    """

    def __init__(self):
        self._landing_url_name = None
        self._landing_app = None
        self._registered = False

    def register_landing_url(self, url_name, app_name):
        """
        Register a URL name as the landing URL.

        Args:
            url_name (str): The URL name to use as landing
            app_name (str): The app name registering the landing URL
        """
        if self._registered:
            logger.warning(
                f"Landing URL already registered by '{self._landing_app}' as '{self._landing_url_name}'. "
                f"Ignoring registration from '{app_name}' for '{url_name}'."
            )
            return False

        self._landing_url_name = url_name
        self._landing_app = app_name
        self._registered = True
        logger.info(f"Landing URL registered: '{url_name}' by app '{app_name}'")
        return True

    def get_landing_url(self):
        """
        Get the registered landing URL.

        Returns:
            str: The landing URL path

        Raises:
            ImproperlyConfigured: If no landing URL is registered
        """
        if not self._registered:
            raise ImproperlyConfigured(
                "No landing URL registered. Make sure one of your apps calls "
                "landing_config.register_landing_url() in its ready() method."
            )

        try:
            return reverse(self._landing_url_name)
        except Exception as e:
            raise ImproperlyConfigured(
                f"Could not reverse landing URL '{self._landing_url_name}' "
                f"registered by app '{self._landing_app}': {e}"
            )

    def get_landing_url_name(self):
        """Get the registered landing URL name."""
        return self._landing_url_name

    def get_landing_app(self):
        """Get the app that registered the landing URL."""
        return self._landing_app

    def is_registered(self):
        """Check if a landing URL is registered."""
        return self._registered

    def clear(self):
        """Clear the registered landing URL (useful for testing)."""
        self._landing_url_name = None
        self._landing_app = None
        self._registered = False


# Global config instance
urls_config = URLsConfig()
