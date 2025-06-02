def vendors(request):
    return {
        "vendor_bootstrap": True,
        "vendor_bootstrap_icons": True,
        "vendor_aos": True,
    }


def header(request):
    return {
        "section_header": True,
        "widget_header_logo": True,
        "widget_header_breadcrumbs": True,
        "widget_header_navigation": True,
    }


def footer(request):
    return {
        "section_footer": True,
    }


def overlay(request):
    return {
        "overlay_back_to_top": True,
        "overlay_whatsapp_call_us": True,
        "overlay_preloader": True,
    }


# def user_preferences(request):
#     if request.user.is_authenticated:
#         return {
#             "user_theme": getattr(request.user, "theme", "default"),
#             "user_timezone": getattr(request.user, "timezone", "UTC"),
#         }
#     return {}
