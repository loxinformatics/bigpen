from django import template
from django.core.cache import cache
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from ..models import OrgDetail, OrgGraphic

register = template.Library()


def get_org_config():
    # Try to get from cache first (cache for 1 hour)
    org_config = cache.get("org_config")

    if org_config is None:
        # Create defaults
        defaults = {
            "ORG_NAME": "A 'Christian Who Codes' Project",
            "ORG_DESCRIPTION": "A 'Christian Who Codes' project built with Django.",
            "ORG_URL": "https://christianwhocodes.space",
            "ORG_THEME_COLOR": "green",
            "ORG_LOGO": static("base/img/logo.png"),
            "ORG_FAVICON": static("base/img/favicon.ico"),
            "ORG_APPLE_TOUCH_ICON": static("base/img/apple-touch-icon.png"),
            "ORG_COVER_IMAGE": static("base/img/cover.png"),
        }

        # Get database values
        org_details = {
            f"{detail.name.upper()}": detail.value
            for detail in OrgDetail.objects.only("name", "value")
        }
        org_graphics = {
            f"{graphic.name.upper()}": graphic.image.url
            for graphic in OrgGraphic.objects.only("name", "image")
        }

        # Merge everything
        defaults.update(org_details)
        defaults.update(org_graphics)

        org_config = defaults

        # Cache for 1 hour
        cache.set("org_config", org_config, 3600)

    return org_config


def get_org_detail(name, default=""):
    config = get_org_config()
    return config.get(name.upper(), default)


@register.simple_tag
def org_meta():
    """
    Render all standard meta tags as HTML using get_org_detail().
    Usage: {% org_meta %}
    """
    html = f"""
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <meta name="theme-color" content="{get_org_detail("ORG_THEME_COLOR", "#000")}" />
    <meta name="author" content="{get_org_detail("ORG_NAME")}" />
    <meta name="description" content="{get_org_detail("ORG_DESCRIPTION")}" />
    <meta name="keywords" content="{get_org_detail("ORG_NAME")}" />
    
    <!-- Twitter -->
    <meta name="twitter:card" content="{get_org_detail("ORG_DESCRIPTION")}" />
    <meta name="twitter:site" content="{get_org_detail("ORG_URL")}" />
    <meta name="twitter:title" content="{get_org_detail("ORG_NAME")}" />
    <meta name="twitter:description" content="{get_org_detail("ORG_DESCRIPTION")}" />
    <meta name="twitter:image" content="{get_org_detail("ORG_LOGO")}" />
    <meta name="twitter:image:alt" content="{get_org_detail("ORG_NAME")}" />
    
    <!-- Open Graph -->
    <meta property="og:url" content="{get_org_detail("ORG_URL")}" />
    <meta property="og:org_name" content="{get_org_detail("ORG_NAME")}" />
    <meta property="og:title" content="{get_org_detail("ORG_NAME")}" />
    <meta property="og:image" content="{get_org_detail("ORG_LOGO")}" />
    <meta property="og:locale" content="en_GB" />
    """

    return mark_safe(html.strip())


@register.simple_tag(takes_context=True)
def org_title(context, title=None, separator=" | "):
    """
    Render the full HTML <title> tag with the page title and site name.
    Usage:
      - {% org_title %}                   ← uses context['org_title']
      - {% org_title "Custom Title" %}    ← uses provided title
      - {% org_title "Custom" " - " %}    ← uses custom separator
    """

    org_name = get_org_detail("ORG_NAME")

    if title is None:
        title = context.get("page_title")

    if title:
        full_title = f"{title}{separator}{org_name}"
    else:
        full_title = org_name

    return mark_safe(f"<title>{full_title}</title>")


@register.simple_tag
def org_icons():
    """
    Render <link> tags for the site's favicon and Apple touch icon.
    Usage: {% org_icons %}
    """

    favicon = get_org_detail("ORG_FAVICON")
    apple_icon = get_org_detail("ORG_APPLE_TOUCH_ICON")

    html = f"""
    <link rel="icon" type="image/x-icon" href="{favicon}">
    <link rel="apple-touch-icon" href="{apple_icon}">
    """

    return mark_safe(html.strip())


@register.simple_tag
def org_name():
    """Get org name specifically"""
    return get_org_detail("ORG_NAME")


@register.simple_tag
def org_description():
    """Get org description specifically"""
    return get_org_detail("ORG_DESCRIPTION")


@register.simple_tag
def org_logo():
    """Get org logo URL"""
    return get_org_detail("ORG_LOGO")


@register.simple_tag
def org_cover_image():
    """Get org logo URL"""
    return get_org_detail("ORG_COVER_IMAGE")
