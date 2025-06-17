from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

from ...models import UserRole


class Command(BaseCommand):
    help = "Assign a role to a user"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="Username of the user")
        parser.add_argument("role", type=str, help="Role name to assign")
        parser.add_argument(
            "--create-user",
            action="store_true",
            help="Create user if it does not exist",
        )

    def handle(self, *args, **options):
        username = options["username"]
        role_name = options["role"]
        create_user = options["create_user"]

        try:
            # Check if role exists
            try:
                UserRole.objects.get(name=role_name)
            except UserRole.DoesNotExist:
                raise CommandError(f'Role "{role_name}" does not exist')

            # Get or create user
            try:
                user = get_user_model().objects.get(username=username)
            except get_user_model().DoesNotExist:
                if create_user:
                    user = get_user_model().objects.create_user(username=username)
                    self.stdout.write(f"Created user: {username}")
                else:
                    raise CommandError(
                        f'User "{username}" does not exist. Use --create-user to create.'
                    )

            # Assign role
            old_role = user.get_role()
            user.set_role(role_name)

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully assigned role "{role_name}" to user "{username}"'
                )
            )

            if old_role != "No role assigned":
                self.stdout.write(f"Previous role: {old_role}")

        except Exception as e:
            raise CommandError(f"Failed to assign role: {e}")
