from apps.core.base.navigation import header_nav_registry


header_nav_registry.register("Home", "landing:index", order=0)
header_nav_registry.register("About", "landing:index", fragment="about", order=1)
header_nav_registry.register("Contact", "landing:index", fragment="contact", order=2)
