# schools/migrations/XXXX_setup_school_roles_and_permissions.py
# Generated manually

from django.contrib.auth.models import Permission
from django.db import migrations


def setup_school_roles_and_permissions(apps, schema_editor):
    """Set up school-specific roles and their permissions"""

    # Get model classes
    UserRole = apps.get_model("core", "UserRole")

    # Define roles
    roles = [
        {
            "name": "client",
            "display_name": "Client",
            "has_portal_access": False,
            "is_default_role": True,
            "description": "Regular customer with the ability to browse products, place orders, and manage their own account.",
        },
        {
            "name": "staff_admin",
            "display_name": "Staff",
            "has_portal_access": True,
            "is_default_role": False,
            "description": "Store staff with limited administrative access to manage orders, view customers, and assist with support.",
        },
        {
            "name": "manager_admin",
            "display_name": "Manager",
            "has_portal_access": True,
            "is_default_role": False,
            "description": "Manager with full administrative privileges, including user management, product control, and site settings.",
        },
    ]

    # Define permissions for each role
    portal_site_role_permissions = {
        "manager_admin": [
            "core.add_user",
            "core.change_user",
            "core.delete_user",
            "core.view_user",
            "core.add_userrole",
            "core.change_userrole",
            "core.delete_userrole",
            "core.view_userrole",
            # Add custom app specific portal site permissions here
        ],
        "staff_admin": [
            # Add custom app specific portal site permissions here
        ],
    }

    # Create or update roles
    created_roles = []
    for role_data in roles:
        role, created = UserRole.objects.get_or_create(
            name=role_data["name"],
            defaults={
                "display_name": role_data["display_name"],
                "has_portal_access": role_data["has_portal_access"],
                "is_default_role": role_data["is_default_role"],
                "description": role_data["description"],
            },
        )

        if not created:
            # Update existing role if needed
            role.display_name = role_data["display_name"]
            role.has_portal_access = role_data["has_portal_access"]
            role.is_default_role = role_data["is_default_role"]
            role.description = role_data["description"]
            role.save()

        created_roles.append(role)

    # Set up permissions for each role
    for role in created_roles:
        permissions_list = portal_site_role_permissions.get(role.name, [])

        if permissions_list:
            # Clear existing permissions
            role.permissions.clear()

            # Add new permissions
            valid_permissions = []
            for perm_string in permissions_list:
                try:
                    if "." in perm_string:
                        app_label, codename = perm_string.split(".", 1)
                        permission = Permission.objects.get(
                            content_type__app_label=app_label, codename=codename
                        )
                        valid_permissions.append(permission)
                except Permission.DoesNotExist:
                    # Permission doesn't exist yet, skip it
                    # This can happen if the migration runs before
                    # the app that defines the permission is migrated
                    pass

            if valid_permissions:
                role.permissions.add(*valid_permissions)


def reverse_school_roles_and_permissions(apps, schema_editor):
    """Remove school-specific roles and permissions"""
    UserRole = apps.get_model("core", "UserRole")

    # Delete the roles we created
    school_role_names = ["student", "instructor", "admin"]
    UserRole.objects.filter(name__in=school_role_names).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),  # Make sure core app's UserRole model exists
        ("custom", "0001_initial"),  # Your custom app's initial migration
        ("contenttypes", "0002_remove_content_type_name"),  # Needed for permissions
        ("auth", "0012_alter_user_first_name_max_length"),  # Needed for permissions
    ]

    operations = [
        migrations.RunPython(
            setup_school_roles_and_permissions,
            reverse_school_roles_and_permissions,
        ),
    ]
