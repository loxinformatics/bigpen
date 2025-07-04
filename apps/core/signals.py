import logging

from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.db import transaction
from django.db.models.signals import (
    post_delete,
    post_migrate,
    post_save,
    pre_migrate,
)
from django.dispatch import receiver
from termcolor import colored

from apps.core.models import (
    BASE_DETAIL_CHOICES,
    BASE_IMAGE_CHOICES,
    BaseDetail,
    BaseImage,
)

logger = logging.getLogger(__name__)


@receiver(post_save, sender=BaseDetail)
@receiver(post_delete, sender=BaseDetail)
@receiver(post_save, sender=BaseImage)
@receiver(post_delete, sender=BaseImage)
def clear_base_config_cache(sender, **kwargs):
    """
    Clear 'base_config' cache (for templatetags) and
    'manifest.json' page cache (for ManifestView)
    when BaseDetail or BaseImage changes.
    """
    try:
        # Check if we're using database cache and if the table exists
        from django.db import connection

        cache_backend = (
            getattr(settings, "CACHES", {}).get("default", {}).get("BACKEND", "")
        )
        if "db.DatabaseCache" in cache_backend:
            # Check if cache table exists before trying to use it
            cache_table_name = (
                getattr(settings, "CACHES", {})
                .get("default", {})
                .get("LOCATION", "django_cache")
            )

            with connection.cursor() as cursor:
                # Database-agnostic way to check if table exists
                try:
                    cursor.execute(f"SELECT 1 FROM {cache_table_name} LIMIT 1")
                except Exception:
                    # Table doesn't exist or can't be accessed
                    logger.debug("Cache table doesn't exist yet, skipping cache clear")
                    return

        # Clear the templatetag's cache
        cache.delete("base_config")
        logger.debug(
            colored(
                f"Cleared 'base_config' cache due to {sender.__name__} change", "green"
            )
        )

        # Clear the ManifestView's page cache
        # Since cache_page creates complex cache keys, we'll use a custom cache key
        # for the manifest data instead of relying on page caching
        cache.delete("manifest_data")

        logger.debug(
            colored(
                f"Cleared manifest cache due to {sender.__name__} change",
                "green",
            )
        )

    except Exception as e:
        # Don't log as error during migrations, just debug
        logger.debug(f"Cache clear skipped: {e}")


@receiver(post_migrate)
def setup_core_data(sender, **kwargs):
    """
    Signal to set up core data after migrations are applied.
    This runs after each migration in the 'core' app.
    """
    # Only run for the core app (check both possible app labels)
    if sender.name not in ["apps.core", "core"]:
        return

    logger.info("Setting up core data after migration")

    # Check if we're in a migration context and if our models exist
    try:
        from django.db import connection
        from .models import BaseDetail, BaseImage  # noqa: F401

        # Check if the tables exist before trying to use them
        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT 1 FROM core_basedetail LIMIT 1")
                cursor.execute("SELECT 1 FROM core_baseimage LIMIT 1")
            except Exception:
                # Tables don't exist yet, skip setup
                logger.debug("Core tables don't exist yet, skipping setup")
                return

        # Setup choice instances
        setup_choice_instances()

        # Setup cache table and npm packages (after transaction commits)
        transaction.on_commit(setup_cache_table)
        transaction.on_commit(setup_npm_packages)

    except Exception as e:
        logger.warning(f"Failed to setup core data: {e}")


@receiver(pre_migrate)
def cleanup_core_data(sender, **kwargs):
    """
    Signal to clean up core data before migrations are unapplied.
    This runs before each migration rollback in the 'core' app.
    """
    # Only run for the core app (check both possible app labels)
    if sender.name not in ["apps.core", "core"]:
        return

    # Check if we're rolling back by examining the migration plan
    plan = kwargs.get("plan", [])
    is_rollback = any(not forward for migration, forward in plan)

    if is_rollback:
        logger.info("Cleaning up core data before migration rollback")
        try:
            # Cleanup operations (after transaction commits)
            transaction.on_commit(cleanup_npm_packages)
            transaction.on_commit(drop_cache_table)

        except Exception as e:
            logger.warning(f"Failed to cleanup core data: {e}")


def setup_choice_instances():
    """
    Create instances for all choices in BaseDetail and BaseImage.
    """
    try:
        from .models import BaseDetail, BaseImage

        # Create ORDER_MAPPING for BaseDetail
        base_detail_order_mapping = {
            key: i + 1 for i, (key, _) in enumerate(BASE_DETAIL_CHOICES)
        }

        # Create BaseDetail instances for all choices
        for choice_key, choice_display in BASE_DETAIL_CHOICES:
            BaseDetail.objects.get_or_create(
                name=choice_key,
                defaults={
                    "value": "",  # Empty value as requested
                    "ordering": base_detail_order_mapping.get(choice_key, 999),
                },
            )

        # Create ORDER_MAPPING for BaseImage
        base_image_order_mapping = {
            key: i + 1 for i, (key, _) in enumerate(BASE_IMAGE_CHOICES)
        }

        # Create BaseImage instances for all choices
        for choice_key, choice_display in BASE_IMAGE_CHOICES:
            BaseImage.objects.get_or_create(
                name=choice_key,
                defaults={
                    "image": None,  # Empty image field
                    "ordering": base_image_order_mapping.get(choice_key, 999),
                },
            )

        logger.info("Successfully set up choice instances")

    except Exception as e:
        logger.warning(f"Failed to setup choice instances: {e}")


def setup_npm_packages():
    """
    Setup npm packages by uninstalling all and then installing defaults.
    """
    try:
        # First, uninstall all existing packages
        call_command("npm", "uninstall", "--all", verbosity=0)
        # Then, install the default packages
        call_command("npm", "install", verbosity=0)
    except Exception as e:
        # Log the error but don't fail the migration
        logger.warning(f"Failed to setup npm packages: {e}")
        logger.info("You can manually run: python manage.py npm install")


def setup_cache_table():
    """
    Setup cache table in database
    """
    try:
        # Try to get from settings
        if hasattr(settings, "CACHES"):
            for cache_config in settings.CACHES.values():
                if (
                    cache_config.get("BACKEND")
                    == "django.core.cache.backends.db.DatabaseCache"
                ):
                    call_command("createcachetable")
                    break
    except Exception as e:
        logger.warning(f"Failed to create cache table: {e}")
        logger.info("You can manually run: python manage.py createcachetable")


def cleanup_npm_packages():
    """
    Reverse npm setup by removing all packages.
    """
    try:
        call_command("npm", "uninstall", "--all", verbosity=0)
    except Exception as e:
        logger.warning(f"Failed to cleanup npm packages: {e}")


def drop_cache_table():
    """
    Drop the cache table from the database.
    """
    try:
        from django.db import connection

        cache_table_name = "django_cache"

        # Try to get from settings
        if hasattr(settings, "CACHES"):
            for cache_config in settings.CACHES.values():
                if (
                    cache_config.get("BACKEND")
                    == "django.core.cache.backends.db.DatabaseCache"
                ):
                    cache_table_name = cache_config.get("LOCATION", "django_cache")
                    # Drop table using connection
                    with connection.cursor() as cursor:
                        cursor.execute(f'DROP TABLE IF EXISTS "{cache_table_name}"')
                    break
    except Exception as e:
        logger.warning(f"Failed to drop cache table: {e}")
