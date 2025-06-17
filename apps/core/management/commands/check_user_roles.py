from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Check user role assignments and staff status consistency"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fix",
            action="store_true",
            help="Fix inconsistent staff status based on roles",
        )

    def handle(self, *args, **options):
        fix_issues = options["fix"]

        self.stdout.write("Checking user role assignments...")

        users_without_roles = []
        inconsistent_staff_status = []

        for user in get_user_model().objects.all():
            # Check for users without roles
            if not user.is_superuser:
                role_obj = user.get_role_object()
                if not role_obj:
                    users_without_roles.append(user.username)
                else:
                    # Check staff status consistency
                    if user.is_staff != role_obj.has_portal_access:
                        inconsistent_staff_status.append(
                            {
                                "username": user.username,
                                "current_staff": user.is_staff,
                                "should_be_staff": role_obj.has_portal_access,
                                "role": role_obj.name,
                            }
                        )

        # Report findings
        if users_without_roles:
            self.stdout.write(
                self.style.WARNING(f"Users without roles ({len(users_without_roles)}):")
            )
            for username in users_without_roles:
                self.stdout.write(f"  - {username}")

        if inconsistent_staff_status:
            self.stdout.write(
                self.style.WARNING(
                    f"Users with inconsistent staff status ({len(inconsistent_staff_status)}):"
                )
            )
            for user_data in inconsistent_staff_status:
                self.stdout.write(
                    f"  - {user_data['username']}: "
                    f"staff={user_data['current_staff']} "
                    f"(should be {user_data['should_be_staff']} for role {user_data['role']})"
                )

        # Fix issues if requested
        if fix_issues and inconsistent_staff_status:
            self.stdout.write("Fixing staff status inconsistencies...")

            for user_data in inconsistent_staff_status:
                get_user_model().objects.filter(username=user_data["username"]).update(
                    is_staff=user_data["should_be_staff"]
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Fixed staff status for {len(inconsistent_staff_status)} users"
                )
            )

        if not users_without_roles and not inconsistent_staff_status:
            self.stdout.write(
                self.style.SUCCESS("All user role assignments look good!")
            )
