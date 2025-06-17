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
            **kwargs,
        }
        self._items.append(item)

    def register_dropdown(self, name, icon="", order=0, type="", **kwargs):
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
            **kwargs,
        }
        self._items.append(item)
        return item

    def add_dropdown_item(
        self, parent_name, name, url_name, icon="", fragment=None, **kwargs
    ):
        """
        Add a child item to an existing dropdown parent.

        Args:
            parent_name: Name of the parent dropdown item
            name: Display name for the child item
            url_name: Django URL name for the child
            icon: Icon class string
            fragment: URL fragment (#section)
            **kwargs: Additional attributes
        """
        for item in self._items:
            if item["name"] == parent_name and item["is_dropdown"]:
                child_item = {
                    "name": name,
                    "url_name": url_name,
                    "icon": icon,
                    "fragment": fragment,
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
            **kwargs,
        }
        parent["dropdown_items"].append(child_item)

    def get_items(self):
        return sorted(self._items, key=lambda x: x["order"])


# Global config instances
nav_config = NavigationConfig()

# Example usage:
if __name__ == "__main__":
    print("=== NavigationRegistry Examples with Dropdown ===")

    # Register regular navigation items
    nav_config.register("Home", "home", order=1, icon="bi bi-house")

    # Register dropdown items
    # Method 1: Register with dropdown_items list
    auth_dropdown_items = [
        {"name": "Login", "url_name": "login", "icon": "bi bi-box-arrow-in-right"},
        {"name": "Sign Up", "url_name": "signup", "icon": "bi bi-person-plus"},
    ]
    nav_config.register(
        "Auth",
        dropdown_items=auth_dropdown_items,
        order=2,
        icon="bi bi-person",
        requires_auth=False,
    )

    # Method 2: Register dropdown parent then add children
    profile_dropdown = nav_config.register_dropdown(
        "Profile", order=3, icon="bi bi-person-circle", requires_auth=True
    )
    nav_config.add_dropdown_item(
        "Profile", "Dashboard", "dashboard", icon="bi bi-speedometer2"
    )
    nav_config.add_dropdown_item("Profile", "Portal", "portal", icon="bi bi-door-open")

    # Get sorted navigation items
    nav_items = nav_config.get_items()
    print("Navigation items (sorted by order):")
    for item in nav_items:
        if item["is_dropdown"]:
            print(f"  - {item['name']} (DROPDOWN) - Order: {item['order']}")
            for child in item["dropdown_items"]:
                print(f"    * {child['name']} ({child['url_name']})")
        else:
            print(f"  - {item['name']} ({item['url_name']}) - Order: {item['order']}")

    print("\n" + "=" * 50 + "\n")
