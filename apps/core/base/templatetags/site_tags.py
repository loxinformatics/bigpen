from django import template
from django.core.cache import cache
from django.templatetags.static import static

from ..models import SiteDetail, SiteGraphic

register = template.Library()


@register.simple_tag
def get_site_config():
    """
    Get complete site configuration with caching
    Usage: {% get_site_config as site %}
    """
    # Try to get from cache first (cache for 1 hour)
    site_config = cache.get("site_config")

    if site_config is None:
        # Create defaults
        defaults = {
            "SITE_NAME": "A 'Christian Who Codes' Project",
            "SITE_DESCRIPTION": "A 'Christian Who Codes' project built with Django.",
            "SITE_URL": "https://christianwhocodes.space",
            "SITE_THEME_COLOR": "green",
            "SITE_LOGO": static("base/img/cwc-logo.png"),
            "SITE_FAVICON": static("base/img/cwc-favicon.ico"),
            "SITE_APPLE_TOUCH_ICON": static("base/img/cwc-apple-touch-icon.png"),
        }

        # Get database values
        site_details = {
            f"{detail.name.upper()}": detail.value
            for detail in SiteDetail.objects.all()
        }

        site_graphics = {
            f"{graphic.name.upper()}": graphic.image.url
            for graphic in SiteGraphic.objects.all()
        }

        # Merge everything
        defaults.update(site_details)
        defaults.update(site_graphics)

        site_config = defaults

        # Cache for 1 hour
        cache.set("site_config", site_config, 3600)

    return site_config


@register.simple_tag
def site_detail(name, default=""):
    """
    Get a specific site detail
    Usage: {% site_detail "SITE_NAME" %}
    """
    config = get_site_config()
    return config.get(name.upper(), default)


@register.simple_tag
def site_name():
    """Get site name specifically"""
    return site_detail("SITE_NAME")


@register.simple_tag
def site_description():
    """Get site description specifically"""
    return site_detail("SITE_DESCRIPTION")


@register.simple_tag
def site_logo():
    """Get site logo URL"""
    return site_detail("SITE_LOGO")


@register.simple_tag
def site_favicon():
    """Get site favicon URL"""
    return site_detail("SITE_FAVICON")


@register.inclusion_tag("base/site/meta.html")
def site_meta_tags():
    """
    Render complete meta tags for site
    Usage: {% site_meta_tags %}
    """
    return {"site": get_site_config()}
