# apps/core/config/urls.py (updated version)
import logging

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse

logger = logging.getLogger(__name__)


class URLsConfig:
    """
    Registry for managing landing and login redirect URLs across Django apps.
    Allows apps to register themselves as URL providers.
    """

    def __init__(self):
        # Landing URL registry
        self._landing_url_name = None
        self._landing_app = None
        self._landing_registered = False

        # Login redirect URL registry
        self._login_redirect_url_name = None
        self._login_redirect_app = None
        self._login_redirect_registered = False

    def register_landing_url(self, url_name, app_name):
        """
        Register a URL name as the landing URL.

        Args:
            url_name (str): The URL name to use as landing
            app_name (str): The app name registering the landing URL
        """
        if self._landing_registered:
            logger.warning(
                f"Landing URL already registered by '{self._landing_app}' as '{self._landing_url_name}'. "
                f"Ignoring registration from '{app_name}' for '{url_name}'."
            )
            return False

        self._landing_url_name = url_name
        self._landing_app = app_name
        self._landing_registered = True
        logger.info(f"Landing URL registered: '{url_name}' by app '{app_name}'")
        return True

    def register_login_redirect_url(self, url_name, app_name):
        """
        Register a URL name as the login redirect URL.

        Args:
            url_name (str): The URL name to use for login redirect
            app_name (str): The app name registering the login redirect URL
        """
        if self._login_redirect_registered:
            logger.warning(
                f"Login redirect URL already registered by '{self._login_redirect_app}' as '{self._login_redirect_url_name}'. "
                f"Ignoring registration from '{app_name}' for '{url_name}'."
            )
            return False

        self._login_redirect_url_name = url_name
        self._login_redirect_app = app_name
        self._login_redirect_registered = True
        logger.info(f"Login redirect URL registered: '{url_name}' by app '{app_name}'")
        return True

    def get_landing_url(self):
        """
        Get the registered landing URL.

        Returns:
            str: The landing URL path

        Raises:
            ImproperlyConfigured: If no landing URL is registered
        """
        if not self._landing_registered:
            raise ImproperlyConfigured(
                "No landing URL registered. Make sure one of your apps calls "
                "urls_config.register_landing_url() in its ready() method."
            )

        try:
            return reverse(self._landing_url_name)
        except Exception as e:
            raise ImproperlyConfigured(
                f"Could not reverse landing URL '{self._landing_url_name}' "
                f"registered by app '{self._landing_app}': {e}"
            )

    def get_login_redirect_url(self):
        """
        Get the registered login redirect URL.

        Returns:
            str: The login redirect URL path

        Raises:
            ImproperlyConfigured: If no login redirect URL is registered
        """
        if not self._login_redirect_registered:
            raise ImproperlyConfigured(
                "No login redirect URL registered. Make sure one of your apps calls "
                "urls_config.register_login_redirect_url() in its ready() method."
            )

        try:
            return reverse(self._login_redirect_url_name)
        except Exception as e:
            raise ImproperlyConfigured(
                f"Could not reverse login redirect URL '{self._login_redirect_url_name}' "
                f"registered by app '{self._login_redirect_app}': {e}"
            )

    def get_landing_url_name(self):
        """Get the registered landing URL name."""
        return self._landing_url_name

    def get_login_redirect_url_name(self):
        """Get the registered login redirect URL name."""
        return self._login_redirect_url_name

    def get_landing_app(self):
        """Get the app that registered the landing URL."""
        return self._landing_app

    def get_login_redirect_app(self):
        """Get the app that registered the login redirect URL."""
        return self._login_redirect_app

    def is_landing_registered(self):
        """Check if a landing URL is registered."""
        return self._landing_registered

    def is_login_redirect_registered(self):
        """Check if a login redirect URL is registered."""
        return self._login_redirect_registered

    def clear(self):
        """Clear all registered URLs (useful for testing)."""
        # Landing URL
        self._landing_url_name = None
        self._landing_app = None
        self._landing_registered = False

        # Login redirect URL
        self._login_redirect_url_name = None
        self._login_redirect_app = None
        self._login_redirect_registered = False

    def clear_landing(self):
        """Clear only the landing URL registration."""
        self._landing_url_name = None
        self._landing_app = None
        self._landing_registered = False

    def clear_login_redirect(self):
        """Clear only the login redirect URL registration."""
        self._login_redirect_url_name = None
        self._login_redirect_app = None
        self._login_redirect_registered = False

    def get_login_redirect_url_safe(self):
        """
        Get the login redirect URL with automatic fallback.

        Returns:
            str: The login redirect URL path, with fallbacks to the registered
                 landing URL or '/dashboard/' default
        """
        try:
            return self.get_login_redirect_url()
        except ImproperlyConfigured:
            # Fallback to landing URL if available
            try:
                return self.get_landing_url()
            except ImproperlyConfigured:
                # Final fallback
                return "/"


# Global config instance
urls_config = URLsConfig()
