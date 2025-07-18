from settings.core.conf import *  # noqa: F403

INSTALLED_APPS.append("apps.custom")  # noqa: F405

# Groups and Permissions Configuration
GROUPS_PERMISSIONS = {
    "superuser": [
        "ecommerce.add_headstaff",
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
