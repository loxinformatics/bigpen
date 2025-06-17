from django import template

register = template.Library()


@register.inclusion_tag("core/partials/modal_auth.html")
def modal_auth():
    pass
