from django import template

register = template.Library()


@register.inclusion_tag("base/vendor/bootstrap.html")
def bootstrap():
    """Enable Bootstrap CSS/JS"""
    pass


@register.inclusion_tag("base/vendor/bootstrap-icons.html")
def bootstrap_icons():
    """Enable Bootstrap Icons"""
    pass


@register.inclusion_tag("base/vendor/aos.html")
def aos():
    """Enable AOS (Animate On Scroll)"""
    pass
