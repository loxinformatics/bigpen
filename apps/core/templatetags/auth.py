from django import template
from django.urls import NoReverseMatch, reverse

from ..management.config.auth import auth_config

register = template.Library()


# URL mappings for auth pages
URL_MAPPINGS = {
    "signin": "signin",
    "signup": "signup",
    "logout": "signout",  # Note: logout maps to signout
    "profile_update": "base:profile",
    "password_reset": "base:password_reset",
    "email_verification": "base:email_verify",
}


@register.simple_tag
def auth_url(page_name):
    """
    Get the URL for an auth page if it's enabled.

    Usage:
    {% auth_url 'signin' %}
    {% auth_url 'signup' %}
    """
    if not auth_config.is_enabled(page_name):
        return ""

    url_name = URL_MAPPINGS.get(page_name)
    if url_name:
        try:
            return reverse(url_name)
        except NoReverseMatch:
            return ""
    return ""


@register.simple_tag
def is_auth_enabled(page_name):
    """
    Check if an auth page is enabled.

    Usage:
    {% is_auth_enabled 'signin' %}
    """
    return auth_config.is_enabled(page_name)


@register.simple_tag
def enabled_auth_pages():
    """
    Get list of all enabled auth pages.

    Usage:
    {% enabled_auth_pages %}
    """
    return auth_config.get_enabled_pages()


@register.simple_tag
def auth_urls():
    """
    Get dictionary of all enabled auth URLs.

    Usage:
    {% auth_urls as urls %}
    {{ urls.signin }}
    """
    enabled_pages = auth_config.get_enabled_pages()
    auth_urls_dict = {}

    for page_name in enabled_pages:
        url_name = URL_MAPPINGS.get(page_name)
        if url_name:
            try:
                auth_urls_dict[page_name] = reverse(url_name)
            except NoReverseMatch:
                continue

    return auth_urls_dict


# Convenience tags for common checks
@register.simple_tag
def has_signin():
    """Check if signin is enabled."""
    return auth_config.is_enabled("signin")


@register.simple_tag
def has_signup():
    """Check if signup is enabled."""
    return auth_config.is_enabled("signup")


@register.simple_tag
def has_logout():
    """Check if logout is enabled."""
    return auth_config.is_enabled("logout")


@register.simple_tag
def has_profile_update():
    """Check if profile update is enabled."""
    return auth_config.is_enabled("profile_update")


@register.simple_tag
def has_password_reset():
    """Check if password reset is enabled."""
    return auth_config.is_enabled("password_reset")


@register.simple_tag
def has_email_verification():
    """Check if email verification is enabled."""
    return auth_config.is_enabled("email_verification")


# Username field configuration tags
@register.simple_tag
def username_label():
    """Get the configured username field label."""
    return auth_config.get_username_label()


@register.simple_tag
def username_placeholder():
    """Get the configured username field placeholder."""
    return auth_config.get_username_placeholder()


@register.simple_tag
def username_config():
    """Get the complete username field configuration."""
    return auth_config.get_username_config()


@register.simple_tag
def global_auth_config(key=None):
    """
    Get global auth configuration.

    Usage:
    {% global_auth_config %}
    {% global_auth_config 'username_field_label' %}
    """
    return auth_config.get_global_config(key)


# Filter versions for use in conditional statements
@register.filter
def auth_enabled(page_name):
    """
    Filter version of is_auth_enabled for use in if statements.

    Usage:
    {% if 'signin'|auth_enabled %}
    """
    return auth_config.is_enabled(page_name)
