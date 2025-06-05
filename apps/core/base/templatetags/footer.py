from django import template

register = template.Library()


# -- Static --
@register.inclusion_tag("base/footer/static.html", takes_context=True)
def footer_static(context):
    return {
        "show_footer": context.get("show_footer", True),
        "footer_newsletter": context.get("footer_newsletter", True),
        "footer_top": context.get("footer_top", True),
        "footer_copyright": context.get("footer_copyright", True),
    }


# -- Content --
@register.inclusion_tag("base/footer/content.html", takes_context=True)
def footer(context):
    return {
        "show_footer": context.get("show_footer", True),
        "footer_newsletter": context.get("footer_newsletter", True),
        "footer_top": context.get("footer_top", True),
        "footer_copyright": context.get("footer_copyright", True),
    }
