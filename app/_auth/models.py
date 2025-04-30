from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models
from django.db.models.signals import post_migrate, pre_delete, pre_save
from django.dispatch import receiver

from .apps import PROTECTED_GROUP_IDS, PROTECTED_GROUPS


class UserGroup(Group):
    class Meta:
        proxy = True
        verbose_name = "User group"
        verbose_name_plural = "User groups"

    def is_protected(self):
        return self.name in PROTECTED_GROUPS.values()

    def is_default_group(self):
        return self.is_protected()

    is_default_group.boolean = True  # Shows icon in admin
    is_default_group.short_description = "Default Group"  # Column header in admin

    def clean(self):
        super().clean()
        if not self.pk:  # Only for new groups
            if UserGroup.objects.filter(name=self.name).exists():
                raise ValidationError(
                    f"A group with name '{self.name}' already exists."
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


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


class User(AbstractUser):
    # Name field that automatically combines first_name and last_name
    @property
    def name(self):
        """Full name (first and last name combined, read-only)."""
        return f"{self.first_name} {self.last_name}".strip()

    email = models.EmailField(
        unique=True,
        help_text="Required. Enter a valid email address."
    )

    # profile
    image = models.ImageField(
        upload_to="images/users/",
        help_text="Upload a profile image (recommended size: 600x600). [Optional]",
        blank=True,
        null=True,
        verbose_name="Profile image",
    )
    title = models.CharField(
        max_length=100,
        blank=True,
        help_text="Enter your professional title or role. [Optional]"
    )
    description = models.TextField(
        blank=True,
        help_text="Add a short bio or description. [Optional]"
    )

    # Socials
    twitter_x = models.URLField(
        blank=True,
        help_text="Link to your Twitter/X profile. [Optional]"
    )
    facebook = models.URLField(
        blank=True,
        help_text="Link to your Facebook profile. [Optional]"
    )
    instagram = models.URLField(
        blank=True,
        help_text="Link to your Instagram profile. [Optional]"
    )
    linkedin = models.URLField(
        blank=True,
        help_text="Link to your LinkedIn profile. [Optional]"
    )
    github = models.URLField(
        blank=True,
        help_text="Link to your GitHub profile. [Optional]"
    )
    youtube = models.URLField(
        blank=True,
        help_text="Link to your YouTube channel. [Optional]"
    )
    website = models.URLField(
        blank=True,
        help_text="Link to your personal or professional website. [Optional]"
    )

    def __str__(self):
        return f"{self.name}"