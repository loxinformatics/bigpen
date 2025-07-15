from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ValidationError
from django.db import models

# from django.dispatch import receiver
from apps.core.models.abstract import Ordering


class User(AbstractUser, Ordering):
    """Custom User model with group-based permissions and staff status management"""

    # 👇make email optional
    email = models.EmailField(blank=True, null=True)
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "auth_user"
        ordering = ["order", "username"]

    def clean(self):
        """Validate group assignments according to business rules"""
        super().clean()

        # Get group names from the many-to-many field
        if self.pk:  # Only check if user exists (has been saved)
            group_names = set(self.groups.values_list("name", flat=True))
            self._validate_group_combinations(group_names)

    def _validate_group_combinations(self, group_names):
        """Validate that group combinations follow business rules"""
        exclusive_groups = {"standard", "manager", "superuser"}
        staff_groups = {"normal_staff", "blogger_staff"}

        # Check for exclusive groups
        exclusive_found = group_names.intersection(exclusive_groups)
        if len(exclusive_found) > 1:
            raise ValidationError(
                f"User can only belong to one of these groups: {', '.join(exclusive_groups)}. "
                f"Found: {', '.join(exclusive_found)}"
            )

        # Check if exclusive group is mixed with others
        if exclusive_found:
            exclusive_group = list(exclusive_found)[0]
            other_groups = group_names - {exclusive_group}
            if other_groups:
                raise ValidationError(
                    f"'{exclusive_group}' group cannot be combined with other groups. "
                    f"Found additional groups: {', '.join(other_groups)}"
                )

        # If no exclusive groups, ensure only staff groups are present
        elif group_names:
            invalid_combinations = group_names - staff_groups
            if invalid_combinations:
                raise ValidationError(
                    f"Invalid group combination. When not using exclusive groups "
                    f"(standard, manager, superuser), only staff groups are allowed: "
                    f"{', '.join(staff_groups)}. Found invalid: {', '.join(invalid_combinations)}"
                )

    def save(self, *args, **kwargs):
        """Custom save method to handle default group assignment and staff status"""
        is_new_user = self.pk is None

        # Set default values for new users
        if is_new_user:
            if self.is_superuser:
                # Superusers get superuser group by default
                self.is_staff = True
            else:
                # Regular users get standard group by default
                self.is_staff = False

        # Call the parent save method first
        super().save(*args, **kwargs)

        # Handle group assignment for new users
        if is_new_user:
            if self.is_superuser:
                superuser_group, created = Group.objects.get_or_create(name="superuser")
                self.groups.set([superuser_group])
            else:
                standard_group, created = Group.objects.get_or_create(name="standard")
                self.groups.set([standard_group])
