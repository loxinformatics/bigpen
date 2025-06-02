class NavigationRegistry:
    def __init__(self):
        self._items = []

    def register(self, name, url_name, order=0, fragment=None, **kwargs):
        self._items.append(
            {
                "name": name,
                "url_name": url_name,
                "order": order,
                "fragment": fragment,
                **kwargs,
            }
        )

    def get_items(self):
        return sorted(self._items, key=lambda x: x["order"])


# Global registry instance
header_nav_registry = NavigationRegistry()
