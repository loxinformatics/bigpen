from django import template

register = template.Library()


@register.filter
def has_role_permission(user, permission):
    """Template filter to check if user has permission through their role"""
    if user.is_superuser:
        return True
    return user.has_role_permission(permission)


@register.simple_tag
def get_user_role_permissions(user):
    """Get all permissions for a user's role"""
    return user.get_role_permissions()
