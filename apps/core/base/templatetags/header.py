from django import template
from django.urls import NoReverseMatch, reverse

from ..nav_registry import header_nav_registry

register = template.Library()


# -- Static --
@register.inclusion_tag("base/header/static.html", takes_context=True)
def header_static(context):
    return {
        "header_logo": context.get("header_logo", True),
        "header_navigation": context.get("header_navigation", True),
        "header_cta_button": context.get("header_cta_button", True),
    }


# -- Content --
@register.inclusion_tag("base/header/content.html", takes_context=True)
def header_content(context):
    nav_items = []
    for item in header_nav_registry.get_items():
        try:
            url = reverse(item["url_name"])
            if item.get("fragment"):
                url += f"#{item['fragment']}"

            nav_items.append(
                {
                    "name": item["name"],
                    "url": url,
                }
            )
        except NoReverseMatch:
            continue

    return {
        "header_logo": context.get("header_logo", True),
        "header_navigation": context.get("header_navigation", True),
        "nav_items": nav_items,
        "header_cta_button": context.get("header_cta_button", True),
    }
