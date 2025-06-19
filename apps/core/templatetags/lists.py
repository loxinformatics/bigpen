from django import template

from ..models import ListItem

register = template.Library()


@register.simple_tag()
def list_features():
    return ListItem.objects.filter(category__name="Features")


@register.simple_tag()
def list_faq():
    return ListItem.objects.filter(category__name="FAQ")
