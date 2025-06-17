import logging

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver
from termcolor import colored

from .models import BaseDetail, BaseImage

logger = logging.getLogger(__name__)


@receiver(post_save, sender=BaseDetail)
@receiver(post_delete, sender=BaseDetail)
@receiver(post_save, sender=BaseImage)
@receiver(post_delete, sender=BaseImage)
def clear_base_config_cache(sender, **kwargs):
    """
    Clear 'base_config' cache (for templatetags) and
    'manifest.json' page cache (for ManifestView)
    when BaseDetail or BaseImage changes.
    """
    try:
        # Clear the templatetag's cache
        cache.delete("base_config")
        logger.debug(
            colored(
                f"Cleared 'base_config' cache due to {sender.__name__} change", "green"
            )
        )

        # Clear the ManifestView's page cache
        # Since cache_page creates complex cache keys, we'll use a custom cache key
        # for the manifest data instead of relying on page caching
        cache.delete("manifest_data")

        logger.debug(
            colored(
                f"Cleared manifest cache due to {sender.__name__} change",
                "green",
            )
        )

    except Exception as e:
        logger.error(colored(f"Error clearing cache: {e}", "red"))


@receiver(m2m_changed, sender=get_user_model().groups.through)
def update_user_staff_status_on_group_change(
    sender, instance, action, pk_set, **kwargs
):
    """Update user staff status when group membership changes"""

    # Only handle post_add and post_remove actions
    if action not in ["post_add", "post_remove", "post_clear"]:
        return

    try:
        # Skip superusers
        if instance.is_superuser:
            return

        # Get the user's current role
        role_obj = instance.get_role_object()

        if role_obj:
            # Update staff status based on role
            new_staff_status = role_obj.has_portal_access
        else:
            # No role assigned, remove staff status
            new_staff_status = False

        # Update if changed
        if instance.is_staff != new_staff_status:
            get_user_model().objects.filter(pk=instance.pk).update(
                is_staff=new_staff_status
            )

            action_desc = {
                "post_add": "added to group",
                "post_remove": "removed from group",
                "post_clear": "cleared from all groups",
            }.get(action, action)

            logger.info(
                colored(
                    f"Updated staff status for user {instance.username} to {new_staff_status} "
                    f"after being {action_desc}",
                    "cyan",
                )
            )

    except Exception as e:
        logger.error(
            colored(
                f"Error updating staff status for user {instance.username} on group change: {e}",
                "red",
            )
        )
