from apps.core.base.nav_registry import header_nav_registry

header_nav_registry.register("Logout", "auth:signout", type="signout", order=76)
