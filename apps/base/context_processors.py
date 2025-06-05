from django.urls import NoReverseMatch, reverse

from .nav_registry import header_nav_registry


def header(request):
    return {
        "show_header": True,
        "header_logo": True,
        "header_navigation": True,
        "header_auth_btn": True,
    }


def navigation(request):
    header_nav_items = []
    for item in header_nav_registry.get_items():
        try:
            url = reverse(item["url_name"])
            if item.get("fragment"):
                url += f"#{item['fragment']}"

            header_nav_items.append(
                {
                    "name": item["name"],
                    "url": url,
                    "type": item.get("type", ""),
                }
            )
        except NoReverseMatch:
            continue

    return {
        "header_nav_items": header_nav_items,
    }


def hero(request):
    return {
        "show_hero": False,
        "hero_btn_1": True,
        "hero_btn_1_login_required": False,
        "hero_btn_1_icon": "",
        "hero_btn_1_name": "Dashboard",
        "hero_btn_1_url_path": "/dashboard/",
        "hero_btn_2": False,
        "hero_btn_2_login_required": False,
        "hero_btn_2_icon": "",
        "hero_btn_2_name": "",
        "hero_btn_2_url_path": "",
    }


def auth(request):
    return {
        "show_auth": False,
        "auth_sigin": False,
        "auth_signup": False,
    }


def footer(request):
    return {
        "show_footer": True,
        "footer_newsletter": True,
        "footer_top": True,
        "footer_copyright": True,
    }


def overlay(request):
    return {
        "overlay_back_to_top": True,
        "overlay_whatsapp_call_us": True,
        "overlay_preloader": True,
    }
