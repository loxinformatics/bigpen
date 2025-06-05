from django import template

register = template.Library()


# -- Static --
@register.inclusion_tag("base/overlay/static.html", takes_context=True)
def overlay_static(context):
    return {
        "overlay_back_to_top": context.get("overlay_back_to_top", True),
        "overlay_whatsapp_call_us": context.get("overlay_whatsapp_call_us", True),
        "overlay_preloader": context.get("overlay_preloader", True),
    }


# -- Content --
@register.inclusion_tag("base/overlay/component.html", takes_context=True)
def overlay(context):
    return {
        "overlay_back_to_top": context.get("overlay_back_to_top", True),
        "overlay_whatsapp_call_us": context.get("overlay_whatsapp_call_us", True),
        "overlay_preloader": context.get("overlay_preloader", True),
        "header_cta_btn_url_path": context.get("header_cta_btn_url_path", "#"),
    }
