from django.core.management.base import BaseCommand

from ...models import UserRole


class Command(BaseCommand):
    help = "List all available roles and their settings"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            action="store_true",
            help="Show user count for each role",
        )

    def handle(self, *args, **options):
        show_users = options["users"]

        roles = UserRole.objects.all().order_by("name")

        if not roles:
            self.stdout.write(self.style.WARNING("No roles found"))
            return

        self.stdout.write(self.style.SUCCESS("Available Roles:"))
        self.stdout.write("-" * 60)

        for role in roles:
            # Basic role info
            self.stdout.write(f"Name: {role.name}")
            self.stdout.write(f"Display Name: {role.get_display_name()}")
            self.stdout.write(f"Staff Role: {'Yes' if role.is_staff_role else 'No'}")
            self.stdout.write(
                f"Default Role: {'Yes' if role.is_default_role else 'No'}"
            )

            if role.description:
                self.stdout.write(f"Description: {role.description}")

            if show_users:
                user_count = role.user_set.count()
                self.stdout.write(f"Users: {user_count}")

            self.stdout.write("-" * 60)
