from django import template

from ..forms import ContactUsForm

register = template.Library()


@register.simple_tag
def contact_form(field):
    """Contact Form"""

    form = ContactUsForm()
    return form[field]


@register.inclusion_tag("core/partials/form_logout.html")
def logout_form():
    pass
