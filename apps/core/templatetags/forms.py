from django import template

from ..forms import ContactUsForm

register = template.Library()


@register.simple_tag
def form_contact_field(field):
    """Contact Form"""

    form = ContactUsForm()
    return form[field]


@register.inclusion_tag("core/partials/form_logout.html", takes_context=True)
def form_logout(context):
    return {"request": context["request"]}
