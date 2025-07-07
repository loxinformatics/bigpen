from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()




@register.simple_tag
def site_url():
    return settings.SITE_URL or ""


@register.simple_tag
def site_name():
    return settings.SITE_NAME or ""


@register.simple_tag
def site_short_name():
    return settings.SITE_SHORT_NAME or ""


@register.simple_tag
def site_description():
    return settings.SITE_DESCRIPTION


@register.simple_tag
def site_theme_color():
    return settings.SITE_THEME_COLOR or "#ef4444"


@register.simple_tag
def site_keywords():
    return (
        settings.SITE_KEYWORDS or "bigpen,Online BigPen Kenya,ecommerce,loxinformatics"
    )


@register.simple_tag
def site_logo():
    return settings.SITE_LOGO or static("core/img/logo.png")


@register.simple_tag
def site_favicon():
    return mark_safe(
        f"<link rel='icon' type='image/x-icon' href='{settings.SITE_FAVICON or static('core/img/favicon.ico')}'>"
    )


@register.simple_tag
def site_apple_touch_icon():
    return mark_safe(
        f"<link rel='apple-touch-icon' href='{settings.SITE_APPLE_TOUCH_ICON or static('core/img/apple-touch-icon.png')}' sizes='180x180'>"
    )


@register.simple_tag
def site_android_chrome_icon():
    return mark_safe(
        f"<link rel='icon' type='image/png' sizes='192x192' href='{settings.SITE_ANDROID_CHROME_ICON or static('core/img/android-chrome-icon.png')}' />"
    )


@register.simple_tag
def site_mstile():
    return mark_safe(
        f"<meta name='msapplication-TileImage' content='{settings.SITE_MSTILE or static('core/img/mstile.png')}' />"
    )


@register.simple_tag
def site_hero():
    return settings.SITE_HERO or static("core/img/hero.jpg")


# TODO: Automatically generate manifest
@register.simple_tag
def site_manifest():
    return mark_safe(
        f"<link rel='manifest' href='{settings.SITE_MANIFEST or static('core/manifest.webmanifest')}'>"
    )


@register.simple_tag
def site_author():
    return settings.SITE_AUTHOR or "christianwhocodes"


@register.simple_tag
def site_author_url():
    return settings.SITE_AUTHOR_URL or "https://github.com/christianwhocodes"


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
