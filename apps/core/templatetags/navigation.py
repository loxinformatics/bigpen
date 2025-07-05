from django import template
from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe

from ..management.config.navigation import nav_config

register = template.Library()


def should_show_item(item, request):
    """
    Determine if an item should be shown based on auth_status and user authentication.

    Args:
        item: Navigation item dictionary
        request: Django request object

    Returns:
        bool: True if item should be shown, False otherwise
    """
    auth_status = item.get("auth_status", "any")

    if auth_status == "any":
        return True

    if not request:
        return auth_status == "public"

    is_authenticated = request.user.is_authenticated

    if auth_status == "private":
        return is_authenticated
    elif auth_status == "public":
        return not is_authenticated
    else:
        # Default to showing for any unrecognized auth_status
        return True


def build_nav_items(config_items, request=None):
    """
    Build navigation items from config, handling authentication logic.
    """
    nav_items = []

    for item in config_items:
        # Check authentication requirements for the parent item
        if not should_show_item(item, request):
            continue

        if item["is_dropdown"]:
            dropdown_children = []
            for child in item["dropdown_items"]:
                # Check authentication requirements for each child item
                if not should_show_item(child, request):
                    continue

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
                            "auth_status": child.get("auth_status", "any"),
                        }
                    )
                except NoReverseMatch:
                    continue

            # Only show dropdown if it has children
            if dropdown_children:
                nav_items.append(
                    {
                        "name": item["name"],
                        "url": "#",
                        "type": item.get("type", ""),
                        "icon": item.get("icon", ""),
                        "is_dropdown": True,
                        "dropdown_items": dropdown_children,
                        "auth_status": item.get("auth_status", "any"),
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
                        "auth_status": item.get("auth_status", "any"),
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


def render_regular_item(nav_type, item, icon_class=""):
    """
    Render a regular navigation item.
    """
    link_class = "navlink"
    icon_class_attr = f' class="{icon_class}"' if icon_class else ""

    if nav_type == "navbar":
        icon_html = (
            f'<i class="{item["icon"]} fs-6 me-2 {icon_class_attr}"></i>'
            if item["icon"]
            else ""
        )
    elif nav_type == "sidebar":
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
    nav_type = context.get("nav_type", "navbar")
    nav_items = build_nav_items(nav_config.get_items(), request)

    html_items = []
    for item in nav_items:
        if item["is_dropdown"]:
            html_items.append(render_dropdown_item(item, icon_class))
        else:
            html_items.append(render_regular_item(nav_type, item, icon_class))

    html = "\n      ".join(html_items)
    return mark_safe(html.strip())
