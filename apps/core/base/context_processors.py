from django.templatetags.static import static

from .models import SiteDetail


def site(request):
    # Create a dict with default values
    defaults = {
        "SITE_NAME": "A 'Christian Who Codes' Project",
        "SITE_DESCRIPTION": "A 'Christian Who Codes' project built with Django.",
        "SITE_URL": "https://christianwhocodes.space",
        "SITE_THEME_COLOR": "green",
        "SITE_LOGO": static("base/img/cwc-logo.png"),
        "SITE_FAVICON": static("base/img/cwc-favicon.ico"),
        "SITE_APPLE_TOUCH_ICON": static("base/img/cwc-apple-touch-icon.png"),
    }

    # Get all site details from database
    site_details = {
        f"{detail.name.upper()}": detail.value for detail in SiteDetail.objects.all()
    }

    # Update defaults with database values
    defaults.update(site_details)
    return defaults


def sections(request):
    return {
        "section_header": True,
        "section_footer": True,
        "section_aside": False,
    }


def widgets(request):
    return {
        "widget_back_to_top": True,
        "widget_whatsapp_call_us": True,
        "widget_preloader": True,
        "widget_header_logo": True,
        "widget_header_breadcrumbs": True,
        "widget_header_navigation": True,
        # "widget_header_search": True,
    }


# def user_preferences(request):
#     if request.user.is_authenticated:
#         return {
#             "user_theme": getattr(request.user, "theme", "default"),
#             "user_timezone": getattr(request.user, "timezone", "UTC"),
#         }
#     return {}
