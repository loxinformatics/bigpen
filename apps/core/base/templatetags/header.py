from django import template
from django.urls import NoReverseMatch, reverse

from ..nav_registry import header_nav_registry

register = template.Library()


# -- Static --
@register.inclusion_tag("base/header/static.html", takes_context=True)
def header_static(context):
    return {
        "show_header": context.get("show_header", True),
        "header_logo": context.get("header_logo", True),
        "header_navigation": context.get("header_navigation", True),
        "header_cta_btn": context.get("header_cta_btn", True),
    }


# -- Content --
@register.inclusion_tag("base/header/component.html", takes_context=True)
def header(context):
    # Extract request from context
    request = context.get("request")

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
                    "type": item.get("type", ""),
                }
            )
        except NoReverseMatch:
            continue

    return {
        "show_header": context.get("show_header", True),
        "header_logo": context.get("header_logo", True),
        "header_navigation": context.get("header_navigation", True),
        "header_cta_btn": context.get("header_cta_btn", True),
        "header_position": context.get("header_position", "sticky"),
        "nav_items": nav_items,
        "header_cta_btn_icon": context.get("header_cta_btn_icon", ""),
        "header_cta_btn_name": context.get("header_cta_btn_name", "Dashboard"),
        "header_cta_btn_url_path": context.get("header_cta_btn_url_path", "#"),
        "header_cta_btn_login_required": context.get(
            "header_cta_btn_login_required", False
        ),
        "user_is_authenticated": request.user.is_authenticated if request else False,
    }
