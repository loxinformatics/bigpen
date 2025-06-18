class AuthConfig:
    """Simplified auth configuration without role management"""

    def __init__(self):
        self._enabled_pages = {
            "signin": True,
            "signup": True,
            "profile_update": True,
            "password_reset": False,
            "email_verification": False,
            "logout": True,
        }
        self._page_configs = {}
        # Global auth configuration
        self._global_config = {
            "username_field_label": "Username",
            "username_field_placeholder": "Enter your username",
        }

    def enable_page(self, page_name, **config):
        """Enable an auth page with optional configuration."""
        if page_name in self._enabled_pages:
            self._enabled_pages[page_name] = True
            if config:
                self._page_configs[page_name] = config
        else:
            raise ValueError(f"Unknown auth page: {page_name}")

    def disable_page(self, page_name):
        """Disable an auth page."""
        if page_name in self._enabled_pages:
            self._enabled_pages[page_name] = False
            self._page_configs.pop(page_name, None)
        else:
            raise ValueError(f"Unknown auth page: {page_name}")

    def is_enabled(self, page_name):
        """Check if an auth page is enabled."""
        return self._enabled_pages.get(page_name, False)

    def get_enabled_pages(self):
        """Get list of all enabled auth pages."""
        return [page for page, enabled in self._enabled_pages.items() if enabled]

    def get_page_config(self, page_name):
        """Get configuration for a specific page."""
        return self._page_configs.get(page_name, {})

    def configure_page(self, page_name, **config):
        """Configure an auth page without changing its enabled status."""
        if page_name in self._enabled_pages:
            self._page_configs[page_name] = config
        else:
            raise ValueError(f"Unknown auth page: {page_name}")

    def get_all_pages_status(self):
        """Get status of all auth pages."""
        return {
            page: {"enabled": enabled, "config": self._page_configs.get(page, {})}
            for page, enabled in self._enabled_pages.items()
        }

    def bulk_configure(self, pages_config):
        """Configure multiple pages at once."""
        for page_name, config in pages_config.items():
            if page_name not in self._enabled_pages:
                raise ValueError(f"Unknown auth page: {page_name}")

            if "enabled" in config:
                self._enabled_pages[page_name] = config["enabled"]
                config = {k: v for k, v in config.items() if k != "enabled"}

            if config:
                self._page_configs[page_name] = config

    def configure_username_field(self, label=None, placeholder=None):
        """Configure the username field globally."""
        if label is not None:
            self._global_config["username_field_label"] = label
        if placeholder is not None:
            self._global_config["username_field_placeholder"] = placeholder

    def get_username_config(self):
        """Get username field configuration."""
        return self._global_config.copy()

    def get_username_label(self):
        """Get the configured username field label."""
        return self._global_config["username_field_label"]

    def get_username_placeholder(self):
        """Get the configured username field placeholder."""
        return self._global_config["username_field_placeholder"]

    def set_global_config(self, **config):
        """Set global configuration options."""
        self._global_config.update(config)

    def get_global_config(self, key=None):
        """Get global configuration."""
        if key:
            return self._global_config.get(key)
        return self._global_config.copy()


# Global config instance
auth_config = AuthConfig()
