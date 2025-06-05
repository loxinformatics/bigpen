from apps.core.base.nav_registry import header_nav_registry


header_nav_registry.register("Home", "landing:index", fragment="hero",order=0)
header_nav_registry.register("About", "landing:index", fragment="about", order=1)
header_nav_registry.register("Contact", "landing:index", fragment="contact", order=2)
