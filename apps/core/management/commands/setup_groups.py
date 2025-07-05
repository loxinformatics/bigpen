from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create user groups with appropriate permissions"

    def handle(self, *args, **options):
        # Define groups and their permissions
        groups_permissions = {
            "superuser": [
                "ecommerce.add_user",
                "ecommerce.change_user",
                "ecommerce.delete_user",
                "ecommerce.view_user",
                "auth.add_group",
                "auth.change_group",
                "auth.delete_group",
                "auth.view_group",
                "auth.add_permission",
                "auth.change_permission",
                "auth.delete_permission",
                "auth.view_permission",
            ],
            "standard": [],
            "manager": [
                "ecommerce.add_user",
                "ecommerce.change_user",
                "ecommerce.view_user",
                "auth.view_group",
            ],
            "normal_staff": ["ecommerce.view_user"],
            "blogger_staff": ["ecommerce.view_user"],
        }

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
