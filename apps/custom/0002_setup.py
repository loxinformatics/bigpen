# schools/migrations/XXXX_setup_school_roles_and_permissions.py
# Generated manually

from django.contrib.auth.models import Permission
from django.db import migrations


def setup_school_roles_and_permissions(apps, schema_editor):
    """Set up school-specific roles and their permissions"""

    # Get model classes
    UserRole = apps.get_model("core", "UserRole")

    # Define school roles
    school_roles = [
        {
            "name": "student",
            "display_name": "Student",
            "is_staff_role": False,
            "is_default_role": True,
            "description": "Standard student role with basic access for schools",
        },
        {
            "name": "instructor",
            "display_name": "Instructor",
            "is_staff_role": True,
            "is_default_role": False,
            "description": "Teaching staff with course management access for schools",
        },
        {
            "name": "admin",
            "display_name": "Administrator",
            "is_staff_role": True,
            "is_default_role": False,
            "description": "Full administrative access for schools",
        },
    ]

    # Define permissions for each role
    role_permissions = {
        "student": [
            "core.view_user",  # Can view their own profile
            # Add school-specific student permissions here
            # "courses.view_course",
            # "assignments.view_assignment",
        ],
        "instructor": [
            "core.view_user",
            "core.change_user",  # Can edit student profiles
            # Add school-specific instructor permissions here
            # "courses.add_course",
            # "courses.change_course",
            # "courses.view_course",
            # "assignments.add_assignment",
            # "assignments.change_assignment",
            # "assignments.view_assignment",
            # "grades.add_grade",
            # "grades.change_grade",
        ],
        "admin": [
            "core.add_user",
            "core.change_user",
            "core.delete_user",
            "core.view_user",
            "core.add_userrole",
            "core.change_userrole",
            "core.delete_userrole",
            "core.view_userrole",
            # Add school-specific admin permissions here
            # "courses.add_course",
            # "courses.change_course",
            # "courses.delete_course",
            # "courses.view_course",
            # "assignments.add_assignment",
            # "assignments.change_assignment",
            # "assignments.delete_assignment",
            # "assignments.view_assignment",
            # "grades.add_grade",
            # "grades.change_grade",
            # "grades.delete_grade",
            # "grades.view_grade",
        ],
    }

    # Create or update roles
    created_roles = []
    for role_data in school_roles:
        role, created = UserRole.objects.get_or_create(
            name=role_data["name"],
            defaults={
                "display_name": role_data["display_name"],
                "is_staff_role": role_data["is_staff_role"],
                "is_default_role": role_data["is_default_role"],
                "description": role_data["description"],
            },
        )

        if not created:
            # Update existing role if needed
            role.display_name = role_data["display_name"]
            role.is_staff_role = role_data["is_staff_role"]
            role.is_default_role = role_data["is_default_role"]
            role.description = role_data["description"]
            role.save()

        created_roles.append(role)

    # Set up permissions for each role
    for role in created_roles:
        permissions_list = role_permissions.get(role.name, [])

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
        ("schools", "0001_initial"),  # Your schools app's initial migration
        ("contenttypes", "0002_remove_content_type_name"),  # Needed for permissions
        ("auth", "0012_alter_user_first_name_max_length"),  # Needed for permissions
    ]

    operations = [
        migrations.RunPython(
            setup_school_roles_and_permissions,
            reverse_school_roles_and_permissions,
        ),
    ]
