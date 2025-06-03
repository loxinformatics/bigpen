from django import template

register = template.Library()


@register.inclusion_tag("base/overlay/back-to-top/static.html", takes_context=True)
def back_to_top_static(context):
    return {
        "overlay_back_to_top": context.get("overlay_back_to_top", True),
    }


@register.inclusion_tag("base/overlay/back-to-top/template.html", takes_context=True)
def back_to_top_template(context):
    return {
        "overlay_back_to_top": context.get("overlay_back_to_top", True),
    }


@register.inclusion_tag("base/overlay/whatsapp-call-us/static.html", takes_context=True)
def whatsapp_call_us_static(context):
    return {
        "overlay_whatsapp_call_us": context.get("overlay_whatsapp_call_us", True),
    }


@register.inclusion_tag(
    "base/overlay/whatsapp-call-us/template.html", takes_context=True
)
def whatsapp_call_us_template(context):
    return {
        "overlay_whatsapp_call_us": context.get("overlay_whatsapp_call_us", True),
    }


@register.inclusion_tag("base/overlay/preloader/static.html", takes_context=True)
def preloader_static(context):
    return {
        "overlay_preloader": context.get("overlay_preloader", True),
    }


@register.inclusion_tag("base/overlay/preloader/template.html", takes_context=True)
def preloader_template(context):
    return {
        "overlay_preloader": context.get("overlay_preloader", True),
    }
