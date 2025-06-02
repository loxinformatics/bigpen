from django import template
from django.urls import NoReverseMatch, reverse

from ..navigation import header_nav_registry

register = template.Library()


@register.inclusion_tag("base/ui/header/header-navigation.html")
def widget_header_navigation():
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
    return {"header_nav_items": nav_items}
