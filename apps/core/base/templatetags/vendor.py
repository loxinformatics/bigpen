from django import template

register = template.Library()


# -- Static --
@register.inclusion_tag("base/vendor/static.html", takes_context=True)
def vendor_static(context):
    """Enable Vendor CSS/JS"""
    return {
        "vendor_bootstrap": context.get("vendor_bootstrap", True),
        "vendor_bootstrap_icons": context.get("vendor_bootstrap_icons", True),
        "vendor_aos": context.get("vendor_aos", True),
    }
