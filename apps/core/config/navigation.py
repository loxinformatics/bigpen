# config/navigation.py


class NavigationConfig:
    def __init__(self):
        self._items = []

    def register(
        self,
        name,
        url_name=None,
        icon="",
        order=0,
        fragment=None,
        type="",
        dropdown_items=None,
        auth_status="any",  # Changed from requires_auth
        **kwargs,
    ):
        """
        Register a navigation item with optional dropdown support.

        Args:
            name: Display name for the navigation item
            url_name: Django URL name (optional for dropdown parents)
            icon: Icon class string
            order: Sort order
            fragment: URL fragment (#section)
            type: Navigation type (page, admin, etc.)
            dropdown_items: List of child navigation items for dropdown
            auth_status: Authentication requirement - "private", "public", or "any"
            **kwargs: Additional attributes
        """
        item = {
            "name": name,
            "url_name": url_name,
            "icon": icon,
            "order": order,
            "fragment": fragment,
            "type": type,
            "dropdown_items": dropdown_items or [],
            "is_dropdown": bool(dropdown_items),
            "auth_status": auth_status,
            **kwargs,
        }
        self._items.append(item)

    def register_dropdown(
        self, name, icon="", order=0, type="", auth_status="any", **kwargs
    ):
        """
        Register a dropdown parent item without a direct URL.

        Returns the item so you can add children to it.
        """
        item = {
            "name": name,
            "url_name": None,
            "icon": icon,
            "order": order,
            "fragment": None,
            "type": type,
            "dropdown_items": [],
            "is_dropdown": True,
            "auth_status": auth_status,
            **kwargs,
        }
        self._items.append(item)
        return item

    def add_dropdown_item(
        self,
        parent_name,
        name,
        url_name,
        icon="",
        fragment=None,
        auth_status="any",
        **kwargs,
    ):
        """
        Add a child item to an existing dropdown parent.

        Args:
            parent_name: Name of the parent dropdown item
            name: Display name for the child item
            url_name: Django URL name for the child
            icon: Icon class string
            fragment: URL fragment (#section)
            auth_status: Authentication requirement - "private", "public", or "any"
            **kwargs: Additional attributes
        """
        for item in self._items:
            if item["name"] == parent_name and item["is_dropdown"]:
                child_item = {
                    "name": name,
                    "url_name": url_name,
                    "icon": icon,
                    "fragment": fragment,
                    "auth_status": auth_status,
                    **kwargs,
                }
                item["dropdown_items"].append(child_item)
                return

        # If parent doesn't exist, create it
        parent = self.register_dropdown(parent_name, **kwargs)
        child_item = {
            "name": name,
            "url_name": url_name,
            "icon": icon,
            "fragment": fragment,
            "auth_status": auth_status,
            **kwargs,
        }
        parent["dropdown_items"].append(child_item)

    def get_items(self):
        return sorted(self._items, key=lambda x: x["order"])


# Global config instances
nav_config = NavigationConfig()

# Example usage:
if __name__ == "__main__":
    print("=== NavigationRegistry Examples with auth_status ===")

    # Register regular navigation items
    nav_config.register("Home", "home", order=1, icon="bi bi-house", auth_status="any")

    # Register dropdown items for unauthenticated users
    auth_dropdown_items = [
        {
            "name": "Login",
            "url_name": "login",
            "icon": "bi bi-box-arrow-in-right",
            "auth_status": "public",
        },
        {
            "name": "Sign Up",
            "url_name": "signup",
            "icon": "bi bi-person-plus",
            "auth_status": "public",
        },
    ]
    nav_config.register(
        "Auth",
        dropdown_items=auth_dropdown_items,
        order=2,
        icon="bi bi-person",
        auth_status="public",  # Changed from requires_auth=False
    )

    # Register dropdown for authenticated users
    profile_dropdown = nav_config.register_dropdown(
        "Profile",
        order=3,
        icon="bi bi-person-circle",
        auth_status="private",  # Changed from requires_auth=True
    )
    nav_config.add_dropdown_item(
        "Profile",
        "Dashboard",
        "dashboard",
        icon="bi bi-speedometer2",
        auth_status="private",
    )
    nav_config.add_dropdown_item(
        "Profile", "Portal", "portal", icon="bi bi-door-open", auth_status="private"
    )

    # Get sorted navigation items
    nav_items = nav_config.get_items()
    print("Navigation items (sorted by order):")
    for item in nav_items:
        if item["is_dropdown"]:
            print(
                f"  - {item['name']} (DROPDOWN) - Order: {item['order']} - Auth: {item['auth_status']}"
            )
            for child in item["dropdown_items"]:
                print(
                    f"    * {child['name']} ({child['url_name']}) - Auth: {child.get('auth_status', 'any')}"
                )
        else:
            print(
                f"  - {item['name']} ({item['url_name']}) - Order: {item['order']} - Auth: {item['auth_status']}"
            )

    print("\n" + "=" * 50 + "\n")
