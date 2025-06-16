from django import template
from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe

from ..config.navigation import nav_config

register = template.Library()


@register.simple_tag
def navigation(link_class=""):
    """
    Template tag that renders navigation items from the registry.

    Usage in templates:
    {% load navigation %}
    {% navigation %}
    {% navigation link_class="header-navlink" %}
    """
    nav_items = []

    for item in nav_config.get_items():
        try:
            url = reverse(item["url_name"])
            if item.get("fragment"):
                url += f"#{item['fragment']}"

            nav_items.append(
                {
                    "name": item["name"],
                    "url": url,
                    "type": item.get("type", ""),
                }
            )
        except NoReverseMatch:
            continue

    # Generate HTML for each nav item
    html_items = []
    for item in nav_items:
        class_attr = f' class="{link_class}"' if link_class else ""
        html_items.append(
            f'<li><a href="{item["url"]}"{class_attr}>{item["name"]}</a></li>'
        )

    html = "\n      ".join(html_items)
    return mark_safe(html)
