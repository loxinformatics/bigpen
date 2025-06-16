from django import template

from ..forms import ContactUsForm

register = template.Library()


@register.simple_tag
def contact_form(field):
    """Contact Form"""

    form = ContactUsForm()
    return form[field]
