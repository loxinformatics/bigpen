class NavigationConfig:
    def __init__(self):
        self._items = []

    def register(
        self, name, url_name, icon="", order=0, fragment=None, type="", **kwargs
    ):
        self._items.append(
            {
                "name": name,
                "url_name": url_name,
                "icon": icon,
                "order": order,
                "fragment": fragment,
                "type": type,
                **kwargs,
            }
        )

    def get_items(self):
        return sorted(self._items, key=lambda x: x["order"])


# Global config instances
header_nav_config = NavigationConfig()
aside_nav_config = NavigationConfig()

# Example usage:
if __name__ == "__main__":
    # ****************** NavigationRegistry examples ******************
    print("=== NavigationRegistry Examples ===")

    # Register navigation items
    header_nav_config.register("Home", "home", order=1, icon="house")
    header_nav_config.register("About", "about", order=3, type="page")
    header_nav_config.register(
        "Dashboard", "dashboard", order=2, fragment="overview", requires_auth=True
    )
    header_nav_config.register(
        "Contact", "contact", order=4, type="page", external=True
    )
    header_nav_config.register(
        "Admin", "admin", order=10, type="admin", permissions=["admin"]
    )

    # Get sorted navigation items
    nav_items = header_nav_config.get_items()
    print("Navigation items (sorted by order):")
    for item in nav_items:
        print(f"  - {item['name']} ({item['url_name']}) - Order: {item['order']}")

    print("\nNavigation items with extra attributes:")
    for item in nav_items:
        extras = {
            k: v for k, v in item.items() if k not in ["name", "url_name", "order"]
        }
        if extras:
            print(f"  - {item['name']}: {extras}")

    print("\n" + "=" * 50 + "\n")
