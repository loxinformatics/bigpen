from django import template
from django.conf import settings
from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe

from ..config.navigation import nav_config

register = template.Library()


def build_nav_items(config_items, request=None):
    """
    Build navigation items from config, handling authentication logic.
    """
    nav_items = []

    for item in config_items:
        # Check authentication requirements
        if item.get("requires_auth") is not None:
            is_authenticated = request and request.user.is_authenticated
            if item["requires_auth"] and not is_authenticated:
                continue
            if not item["requires_auth"] and is_authenticated:
                continue

        if item["is_dropdown"]:
            dropdown_children = []
            for child in item["dropdown_items"]:
                try:
                    child_url = reverse(child["url_name"])
                    if child.get("fragment"):
                        child_url += f"#{child['fragment']}"
                    dropdown_children.append(
                        {
                            "name": child["name"],
                            "url": child_url,
                            "icon": child.get("icon", ""),
                            "type": child.get("type", ""),
                        }
                    )
                except NoReverseMatch:
                    continue

            if dropdown_children:
                nav_items.append(
                    {
                        "name": item["name"],
                        "url": "#",
                        "type": item.get("type", ""),
                        "icon": item.get("icon", ""),
                        "is_dropdown": True,
                        "dropdown_items": dropdown_children,
                    }
                )
        else:
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
                        "is_dropdown": False,
                    }
                )
            except NoReverseMatch:
                continue

    return nav_items


def render_dropdown_item(item, icon_class=""):
    """
    Render a dropdown menu item without active classes (handled by JavaScript).
    """
    # For aside navigation, use toggle-dropdown-link class
    link_class = "toggle-dropdown-link"
    icon_class_attr = f' class="{icon_class}"' if icon_class else ""

    icon_html = (
        f'<i class="{item["icon"]} navicon {icon_class_attr}"></i>'
        if item["icon"]
        else ""
    )

    children_html = []
    for child in item["dropdown_items"]:
        child_icon_html = f'<i class="{child["icon"]}"></i>' if child["icon"] else ""

        children_html.append(
            f'''
                <li>
                    <a href="{child["url"]}" class="navlink">
                        {child_icon_html}
                        {child["name"]}
                    </a>
                </li>
            '''
        )

    children_html_str = "\n                ".join(children_html)

    return f'''
        <li class="dropdown">
            <a href="#" class="{link_class}">
                {icon_html}
                <span>{item["name"]}</span>
                <i class="bi bi-chevron-down toggle-dropdown"></i>
            </a>
            <ul>
                {children_html_str}
            </ul>
        </li>
    '''


def render_regular_item(item, icon_class=""):
    """
    Render a regular navigation item without active classes (handled by JavaScript).
    """
    link_class = "navlink"
    icon_class_attr = f' class="{icon_class}"' if icon_class else ""

    if settings.NAVIGATION_TYPE == "navbar":
        icon_html = (
            f'<i class="{item["icon"]} fs-6 me-2 {icon_class_attr}"></i>'
            if item["icon"]
            else ""
        )
    elif settings.NAVIGATION_TYPE == "sidebar":
        icon_html = (
            f'<i class="{item["icon"]} navicon {icon_class_attr}"></i>'
            if item["icon"]
            else ""
        )

    return f'''
        <li>
            <a href="{item["url"]}" class="{link_class}">
                {icon_html}
                {item["name"]}
            </a>
        </li>
    '''


@register.simple_tag(takes_context=True)
def navmenu(context, icon_class=""):
    request = context.get("request")
    nav_items = build_nav_items(nav_config.get_items(), request)

    html_items = []
    for item in nav_items:
        if item["is_dropdown"]:
            html_items.append(render_dropdown_item(item, icon_class))
        else:
            html_items.append(render_regular_item(item, icon_class))

    html = "\n      ".join(html_items)
    return mark_safe(html.strip())


@register.simple_tag()
def navigation_type():
    return settings.NAVIGATION_TYPE
