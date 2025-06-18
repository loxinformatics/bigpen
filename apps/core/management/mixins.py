from django.shortcuts import redirect

from apps.core.management.config.urls import urls_config


class AnonymousRequiredMixin:
    """
    Mixin that requires user to be anonymous (not authenticated).
    Redirects authenticated users to the registered login redirect URL.
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_authenticated_redirect_url())
        return super().dispatch(request, *args, **kwargs)

    def get_authenticated_redirect_url(self):
        """
        Get the URL to redirect authenticated users to.
        Uses the registry's safe method with built-in fallbacks.
        """
        return urls_config.get_login_redirect_url_safe()
