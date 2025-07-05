from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create user groups with appropriate permissions from settings"

    def handle(self, *args, **options):
        # Get groups configuration from settings with fallback
        default_groups = {
            "standard": [],
            "staff": ["auth.view_group"],
        }

        groups_permissions = getattr(settings, "GROUPS_PERMISSIONS", default_groups)

        if not groups_permissions:
            self.stdout.write(
                self.style.WARNING(
                    "GROUPS_PERMISSIONS not found in settings. Using default groups."
                )
            )
            groups_permissions = default_groups

        if not isinstance(groups_permissions, dict):
            self.stdout.write(
                self.style.ERROR(
                    "GROUPS_PERMISSIONS must be a dictionary. "
                    "Please check your settings.py file."
                )
            )
            return

        for group_name, permission_codenames in groups_permissions.items():
            # Create or get the group
            group, created = Group.objects.get_or_create(name=group_name)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created group: {group_name}"))
            else:
                self.stdout.write(f"Group already exists: {group_name}")

            # Clear existing permissions and add new ones
            group.permissions.clear()

            for perm_str in permission_codenames:
                app_label, codename = perm_str.split(".")
                try:
                    permission = Permission.objects.get(
                        content_type__app_label=app_label, codename=codename
                    )
                    group.permissions.add(permission)
                    self.stdout.write(f"  Added permission: {perm_str}")
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f"  Permission not found: {perm_str}")
                    )

        self.stdout.write(self.style.SUCCESS("Successfully set up all groups!"))
