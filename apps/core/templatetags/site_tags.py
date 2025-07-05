from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def site_title(context, title=None, separator=" | "):
    """
    Render the full HTML <title> tag with the page title and site name.
    Usage:
      - {% site_title %}                   ← uses context['site_title']
      - {% site_title "Custom Title" %}    ← uses provided title
      - {% site_title "Custom" " - " %}    ← uses custom separator
    """

    site_name = settings.SITE_NAME

    if title is None:
        title = context.get("page_title")

    if title:
        full_title = f"{title}{separator}{site_name}"
    else:
        full_title = site_name

    return mark_safe(f"<title>{full_title}</title>")


@register.simple_tag
def site_url():
    return settings.SITE_URL


@register.simple_tag
def site_name():
    return settings.SITE_NAME


@register.simple_tag
def site_short_name():
    return settings.SITE_SHORT_NAME


@register.simple_tag
def site_description():
    return settings.SITE_DESCRIPTION


@register.simple_tag
def site_theme_color():
    return settings.SITE_THEME_COLOR


@register.simple_tag
def site_keywords():
    return settings.SITE_KEYWORDS


@register.simple_tag
def site_logo():
    return settings.SITE_LOGO


@register.simple_tag
def site_favicon():
    return mark_safe(
        f"<link rel='icon' type='image/x-icon' href='{settings.SITE_FAVICON}'>"
    )


@register.simple_tag
def site_apple_touch_icon():
    return mark_safe(
        f"<link rel='apple-touch-icon' href='{settings.SITE_APPLE_TOUCH_ICON}' sizes='180x180'>"
    )


@register.simple_tag
def site_android_chrome_icon():
    return mark_safe(
        f"<link rel='icon' type='image/png' sizes='192x192' href='{settings.SITE_ANDROID_CHROME_ICON}' />"
    )


@register.simple_tag
def site_mstile():
    return mark_safe(
        f"<meta name='msapplication-TileImage' content='{settings.SITE_MSTILE}' />"
    )


@register.simple_tag
def site_hero():
    return settings.SITE_HERO


# TODO: Automatically generate manifest
@register.simple_tag
def site_manifest():
    return mark_safe(f"<link rel='manifest' href='{settings.SITE_MANIFEST}'>")


@register.simple_tag
def site_author():
    return settings.SITE_AUTHOR


@register.simple_tag
def site_author_url():
    return settings.SITE_AUTHOR_URL


@register.simple_tag
def site_credits():
    author = settings.SITE_AUTHOR
    author_url = settings.SITE_AUTHOR_URL

    class_name = "pe-none" if not author_url or author_url == "#" else ""

    html = (
        f'Designed by <a href="{author_url}" class="{class_name}"><em>{author}</em></a>'
    )
    return mark_safe(html.strip())
