/**
 * Navigation Active State Management
 */
function updateActiveStates() {
  // Remove all active classes first (but preserve open-by-default dropdowns)
  document.querySelectorAll(".navmenu a.active").forEach((link) => {
    link.classList.remove("active");
  });
  document
    .querySelectorAll(".navmenu .dropdown.active:not(.open-by-default)")
    .forEach((dropdown) => {
      dropdown.classList.remove("active");
    });
  document
    .querySelectorAll(".navmenu ul.dropdown-active:not(.open-by-default ul)")
    .forEach((ul) => {
      if (!ul.closest(".open-by-default")) {
        ul.classList.remove("dropdown-active");
      }
    });

  // Find matching links and set active states
  document.querySelectorAll(".navmenu a[href]").forEach((link) => {
    const href = link.getAttribute("href");
    if (!href || href === "#") return;

    // Handle URLs with query parameters (like auth URLs)
    const linkUrl = new URL(href, window.location.origin);
    const currentUrl = new URL(window.location.href);

    const linkPath = linkUrl.pathname;
    const linkHash = linkUrl.hash;
    const currentPathname = currentUrl.pathname;
    const currentHashname = currentUrl.hash;

    // Check for exact match (including hash) or path match
    const isExactMatch =
      linkPath === currentPathname && linkHash === currentHashname;
    const isPathMatch = linkPath === currentPathname && linkPath !== "";
    const isHashMatch =
      currentHashname && linkHash && linkHash === currentHashname;

    if (isExactMatch || isPathMatch || isHashMatch) {
      link.classList.add("active");

      // If this is a dropdown item, also activate the parent dropdown
      const parentDropdown = link.closest(".dropdown");
      if (parentDropdown) {
        parentDropdown.classList.add("active");
        const dropdownUl = parentDropdown.querySelector("ul");
        if (dropdownUl) {
          dropdownUl.classList.add("dropdown-active");
        }

        // Also add active class to the parent dropdown link (including toggle-dropdown-link)
        const parentLink = parentDropdown.querySelector(
          "a.navlink, a.toggle-dropdown-link"
        );
        if (parentLink) {
          parentLink.classList.add("active");
        }
      }
    }
  });
}

/**
 * Aside toggle
 */
const asideToggleBtn = document.querySelector("#aside .aside-toggle");

function asideToggle() {
  document.querySelector("#aside").classList.toggle("aside-show");
  asideToggleBtn.classList.toggle("bi-list");
  asideToggleBtn.classList.toggle("bi-x");
}

if (asideToggleBtn) {
  asideToggleBtn.addEventListener("click", asideToggle);
}

/**
 * Hide mobile nav on same-page/hash links
 */
document.querySelectorAll("#aside #navmenu a").forEach((navmenu) => {
  navmenu.addEventListener("click", () => {
    // Only close aside if this is NOT a dropdown toggle link
    if (
      !navmenu.classList.contains("toggle-dropdown-link") &&
      document.querySelector(".aside-show")
    ) {
      asideToggle();
    }
  });
});

/**
 * Toggle aside nav dropdowns
 */
document
  .querySelectorAll(".aside .navmenu .toggle-dropdown-link")
  .forEach((link) => {
    link.addEventListener("click", function (e) {
      const parentLi = this.closest("li");

      // Prevent actual link behavior
      e.preventDefault();

      // Toggle the parent <li>'s active class
      parentLi.classList.toggle("active");

      // Toggle the next <ul> dropdown
      const dropdown = parentLi.querySelector("ul");
      if (dropdown) {
        dropdown.classList.toggle("dropdown-active");
      }

      e.stopImmediatePropagation();
    });
  });

// Automatically open dropdowns marked with .open-by-default
document
  .querySelectorAll(".aside .navmenu .dropdown.open-by-default")
  .forEach((item) => {
    item.classList.add("active");

    const dropdown = item.querySelector("ul");
    if (dropdown) {
      dropdown.classList.add("dropdown-active");
    }
  });

/**
 * Mobile nav toggle
 */
const headerMobileNavToggleBtn = document.querySelector(
  "#header .mobile-nav-toggle"
);

function mobileNavToogle() {
  document.querySelector("body").classList.toggle("mobile-nav-active");
  headerMobileNavToggleBtn.classList.toggle("bi-list");
  headerMobileNavToggleBtn.classList.toggle("bi-x");
}

if (headerMobileNavToggleBtn) {
  headerMobileNavToggleBtn.addEventListener("click", mobileNavToogle);
}

/**
 * Hide mobile nav on same-page/hash links
 */
document.querySelectorAll("#header #navmenu a").forEach((navmenu) => {
  navmenu.addEventListener("click", () => {
    if (document.querySelector(".mobile-nav-active")) {
      mobileNavToogle();
    }
  });
});

/**
 * Toggle mobile nav dropdowns
 */
document.querySelectorAll(".navmenu .toggle-dropdown").forEach((navmenu) => {
  navmenu.addEventListener("click", function (e) {
    e.preventDefault();
    this.parentNode.classList.toggle("active");
    this.parentNode.nextElementSibling.classList.toggle("dropdown-active");
    e.stopImmediatePropagation();
  });
});

/**
 * Navmenu Scrollspy
 */
let navmenulinks = document.querySelectorAll(".navmenu a");

function navmenuScrollspy() {
  navmenulinks.forEach((navmenulink) => {
    if (!navmenulink.hash) return;
    let section = document.querySelector(navmenulink.hash);
    if (!section) return;
    let position = window.scrollY + 200;
    if (
      position >= section.offsetTop &&
      position <= section.offsetTop + section.offsetHeight
    ) {
      document
        .querySelectorAll(".navmenu a.active")
        .forEach((link) => link.classList.remove("active"));
      navmenulink.classList.add("active");

      // If this is a dropdown item, also activate the parent dropdown
      const parentDropdown = navmenulink.closest(".dropdown");
      if (parentDropdown) {
        parentDropdown.classList.add("active");
        const dropdownUl = parentDropdown.querySelector("ul");
        if (dropdownUl) {
          dropdownUl.classList.add("dropdown-active");
        }

        // Also add active class to the parent dropdown link
        const parentLink = parentDropdown.querySelector("a.navlink");
        if (parentLink) {
          parentLink.classList.add("active");
        }
      }
    } else {
      navmenulink.classList.remove("active");
    }
  });
}

// Initialize active states on page load
window.addEventListener("load", function () {
  updateActiveStates();
  navmenuScrollspy();
});

// Update active states when navigating (for SPAs or hash changes)
window.addEventListener("popstate", updateActiveStates);
window.addEventListener("hashchange", updateActiveStates);

// Update scrollspy on scroll
document.addEventListener("scroll", navmenuScrollspy);

// Optional: Update active states when clicking navigation links
document.querySelectorAll(".navmenu a").forEach((link) => {
  link.addEventListener("click", function () {
    // Small delay to ensure URL has changed
    setTimeout(updateActiveStates, 10);
  });
});


/**
 * Tooltips for Long User Name
 */
function enableTruncationTooltipsforUserName(selector = "#aside .user-name") {
  document.querySelectorAll(selector).forEach((el) => {
    // Remove any existing tooltip to avoid duplicates
    if (el._tooltipInstance) {
      el._tooltipInstance.dispose();
    }

    if (el.scrollWidth > el.clientWidth) {
      el.setAttribute("data-bs-toggle", "tooltip");
      el.setAttribute("data-bs-placement", "top");
      el.setAttribute("title", el.textContent.trim());

      const tooltip = new bootstrap.Tooltip(el);
      el._tooltipInstance = tooltip;
    } else {
      // Clean up attributes if not truncated
      el.removeAttribute("data-bs-toggle");
      el.removeAttribute("data-bs-placement");
      el.removeAttribute("title");
    }
  });
}

enableTruncationTooltipsforUserName();
