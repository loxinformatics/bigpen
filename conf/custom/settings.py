from conf.custom.local_site import *  # noqa: F403
from conf.settings import *  # noqa: F403

# Add ecommerce app
INSTALLED_APPS.append("apps.ecommerce")  # noqa: F405

# Override Navigation type
# NAVIGATION_TYPE = "sidebar"

# Custom user model
AUTH_USER_MODEL = "ecommerce.User"

# Groups and Permissions Configuration
GROUPS_PERMISSIONS = {
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
