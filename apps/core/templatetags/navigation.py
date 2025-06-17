from django import template
from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe

from ..config.navigation import aside_nav_config, header_nav_config

register = template.Library()


@register.simple_tag
def header_navigation(link_class="", icon_class=""):
    """
    Template tag that renders navigation items from the registry.

    Usage in templates:
    {% load navigation %}
    {% header_navigation %}
    {% header_navigation link_class="header-navlink" %}
    """
    nav_items = []

    for item in header_nav_config.get_items():
        try:
            url = reverse(item["url_name"])
            if item.get("fragment"):
                url += f"#{item['fragment']}"

            nav_items.append(
                {
                    "name": item["name"],
                    "url": url,
                    "type": item.get("type", ""),
                    "icon": item.get("icon", ""),
                }
            )
        except NoReverseMatch:
            continue

    # Generate HTML for each nav item
    html_items = []
    for item in nav_items:
        link_class_attr = f' class="{link_class}"' if link_class else ""
        icon_class_attr = f' class="{icon_class}"' if icon_class else ""
        icon_html = (
            f'<i class="{item["icon"]} fs-6 me-2 {icon_class_attr}"></i>'
            if item["icon"]
            else ""
        )

        html_items.append(
            f'''
                <li>
                    <a href="{item["url"]}"{link_class_attr}>
                        {icon_html}
                        <span>{item["name"]}</span>
                    </a>
                </li>
            '''
        )

    html = "\n      ".join(html_items)
    return mark_safe(html.strip())


@register.simple_tag
def aside_navigation(link_class="", icon_class=""):
    nav_items = []

    for item in aside_nav_config.get_items():
        try:
            url = reverse(item["url_name"])
            if item.get("fragment"):
                url += f"#{item['fragment']}"

            nav_items.append(
                {
                    "name": item["name"],
                    "url": url,
                    "type": item.get("type", ""),
                    "icon": item.get("icon", ""),
                }
            )
        except NoReverseMatch:
            continue

    # Generate HTML for each nav item
    html_items = []
    for item in nav_items:
        link_class_attr = f' class="{link_class}"' if link_class else ""
        icon_class_attr = f' class="{icon_class}"' if icon_class else ""
        icon_html = (
            f'<i class="{item["icon"]} navicon {icon_class_attr}"></i>'
            if item["icon"]
            else ""
        )

        html_items.append(
            f'''
                <li>
                    <a href="{item["url"]}"{link_class_attr}>
                        {icon_html}
                        <span>{item["name"]}</span>
                    </a>
                </li>
            '''
        )

    html = "\n      ".join(html_items)
    return mark_safe(html.strip())
