from django.db import IntegrityError
from django.db.models.signals import post_migrate, pre_delete, pre_save
from django.dispatch import receiver

from .apps import PROTECTED_GROUP_IDS, PROTECTED_GROUPS
from .models import UserGroup


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """Ensure protected groups exist after migrations with specific PKs"""
    for group_name, group_id in zip(
        PROTECTED_GROUPS.values(), PROTECTED_GROUP_IDS.values()
    ):
        try:
            UserGroup.objects.get_or_create(id=group_id, defaults={"name": group_name})
        except IntegrityError:
            # If ID is taken, try creating without specific ID
            UserGroup.objects.get_or_create(name=group_name)


@receiver(pre_save, sender=UserGroup)
def prevent_protected_group_changes(sender, instance, **kwargs):
    """Prevent renaming of protected groups"""
    if not instance.pk:  # New group being created
        return

    try:
        old_instance = UserGroup.objects.get(pk=instance.pk)
        if (
            old_instance.name in PROTECTED_GROUPS.values()
            and instance.name != old_instance.name
        ):
            instance.name = old_instance.name  # Revert the name change
    except UserGroup.DoesNotExist:
        pass  # Handle case where group doesn't exist yet


@receiver(pre_delete, sender=UserGroup)
def prevent_protected_group_deletion(sender, instance, **kwargs):
    """Prevent deletion of protected groups"""
    if instance.name in PROTECTED_GROUPS.values():
        raise ValueError(f"Cannot delete protected group: {instance.name}")
