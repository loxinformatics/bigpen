from django import template

register = template.Library()


# -- Static --
@register.inclusion_tag("base/hero-or-breadcrumbs/static.html", takes_context=True)
def hero_or_breadcrumbs_static(context):
    return {
        "hero_or_breadcrumbs": context.get("hero_or_breadcrumbs", "breadcrumbs"),
    }


# -- Content --
@register.inclusion_tag("base/hero-or-breadcrumbs/content.html", takes_context=True)
def hero_or_breadcrumbs_content(context):
    return {
        "hero_or_breadcrumbs": context.get("hero_or_breadcrumbs", "breadcrumbs"),
    }
