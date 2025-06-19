let portfolioData = {
  categories: [],
  items: [],
  currentFilter: "*",
  apiBaseUrl: "/api",
  isotopeInstance: null,
};

let glightboxInstance = null;

// Wait for all deferred scripts to load
document.addEventListener("DOMContentLoaded", function () {
  // Add a small delay to ensure all deferred scripts are loaded
  setTimeout(() => {
    initializePortfolio();
  }, 100);
});

async function initializePortfolio() {
  try {
    await loadPortfolioCategories();
    await loadPortfolioItems();
    renderPortfolioFilters();
    renderPortfolioItems();
    attachPortfolioEventListeners();
  } catch (error) {
    console.error("Error initializing portfolio:", error);
  }
}

async function loadPortfolioCategories() {
  try {
    const response = await fetch(
      `${portfolioData.apiBaseUrl}/portfolio/?is_active=true`
    );
    if (!response.ok) throw new Error("Failed to load categories");
    portfolioData.categories = await response.json();
  } catch (error) {
    console.error("Error loading categories:", error);
    portfolioData.categories = [];
  }
}

async function loadPortfolioItems() {
  try {
    const itemPromises = portfolioData.categories.map(async (category) => {
      const response = await fetch(
        `${portfolioData.apiBaseUrl}/portfolio/${category.id}/items/`
      );
      if (!response.ok)
        throw new Error(`Failed to load items for category ${category.id}`);
      const categoryItems = await response.json();
      return categoryItems.map((item) => ({
        ...item,
        category_id: category.id,
        category_name: category.name,
      }));
    });

    const itemArrays = await Promise.all(itemPromises);
    portfolioData.items = itemArrays.flat();
  } catch (error) {
    console.error("Error loading items:", error);
    portfolioData.items = [];
  }
}

function renderPortfolioFilters() {
  const filtersContainer = document.getElementById("categoryFilters");
  if (!filtersContainer) return;

  const allFilter = document.createElement("li");
  allFilter.setAttribute("data-filter", "*");
  allFilter.classList.add("filter-active");
  allFilter.innerHTML = '<i class="bi bi-grid me-2"></i>All Categories';

  filtersContainer.innerHTML = "";
  filtersContainer.appendChild(allFilter);

  portfolioData.categories.forEach((category) => {
    const filter = document.createElement("li");
    filter.setAttribute("data-filter", `.filter-category-${category.id}`);
    filter.innerHTML = `<i class="${category.bootstrap_icon} me-2"></i>${category.name}`;
    filtersContainer.appendChild(filter);
  });
}

function renderPortfolioItems() {
  const container = document.getElementById("categoryItemsContainer");
  if (!container) return;

  container.innerHTML = "";

  portfolioData.items.forEach((item) => {
    const el = createPortfolioItemElement(item);
    container.appendChild(el);
  });

  // Process HTMX attributes on the new content
  if (typeof htmx !== "undefined") {
    htmx.process(container);
  }

  // Use your original isotope initialization approach
  initializeIsotopeOriginal(container);
  initializeGLightbox();
}

function initializeIsotopeOriginal(container) {
  // Destroy existing instance
  if (portfolioData.isotopeInstance) {
    portfolioData.isotopeInstance.destroy();
    portfolioData.isotopeInstance = null;
  }

  // Check if Isotope is available
  if (typeof Isotope === "undefined") {
    console.error("Isotope is not loaded");
    return;
  }

  // Get layout settings from data attributes or use defaults
  const isotopeLayout = container.closest(".isotope-layout");
  let layout = isotopeLayout?.getAttribute("data-layout") ?? "masonry";
  let filter = isotopeLayout?.getAttribute("data-default-filter") ?? "*";
  let sort = isotopeLayout?.getAttribute("data-sort") ?? "original-order";

  // Use imagesLoaded before initializing Isotope (your original approach)
  if (typeof imagesLoaded !== "undefined") {
    imagesLoaded(container, function () {
      portfolioData.isotopeInstance = new Isotope(container, {
        itemSelector: ".isotope-item",
        layoutMode: layout,
        filter: filter,
        sortBy: sort,
        percentPosition: true,
        masonry: {
          columnWidth: ".isotope-item",
          gutter: 0,
        },
        transitionDuration: "0.4s",
      });
    });
  } else {
    // Fallback if imagesLoaded is not available
    setTimeout(() => {
      portfolioData.isotopeInstance = new Isotope(container, {
        itemSelector: ".isotope-item",
        layoutMode: layout,
        filter: filter,
        sortBy: sort,
        percentPosition: true,
        masonry: {
          columnWidth: ".isotope-item",
          gutter: 0,
        },
        transitionDuration: "0.4s",
      });
    }, 500);
  }
}

function createPortfolioItemElement(item) {
  const mainImage =
    item.main_image || "/lib/static/core/img/placeholder-img.png";

  const wrapper = document.createElement("div");
  wrapper.className = `col-lg-6 col-md-6 portfolio-item isotope-item filter-category-${item.category_id}`;
  wrapper.innerHTML = `
    <div class="portfolio-wrap">
      <img src="${mainImage}" class="img-fluid" alt="${item.name}" loading="lazy">
      <div class="portfolio-info">
        <div class="content">
          <span class="category">${item.category_name}</span>
          <h4>${item.name}</h4>
          <div class="portfolio-links">
            <a href="${mainImage}" 
               class="portfolio-lightbox" 
               title="${item.name}"
               data-category="${item.category_id}"
               data-item-id="${item.id}">
               <i class="bi bi-plus-lg"></i>
            </a>
            <a
              class="btn"
              hx-get="/swaps/portfolio/item/${item.id}/"
              hx-target="#portfolio-detail-modal-body"
              data-bs-toggle="modal"
              data-bs-target="#portfolio-detail-modal"
              title="View Details">
                <i class="bi bi-arrow-right"></i>
            </a>
          </div>
        </div>
      </div>
    </div>
  `;
  return wrapper;
}

function attachPortfolioEventListeners() {
  // Look for isotope-filters first (your HTML structure), fallback to portfolio-filters
  const filterButtons = document.querySelectorAll(
    ".isotope-filters li, .portfolio-filters li"
  );

  filterButtons.forEach((btn) => {
    btn.addEventListener("click", function () {
      // Remove active class from all filters
      filterButtons.forEach((f) => f.classList.remove("filter-active"));
      this.classList.add("filter-active");

      const filterValue = this.getAttribute("data-filter");
      portfolioData.currentFilter = filterValue;

      if (portfolioData.isotopeInstance) {
        portfolioData.isotopeInstance.arrange({ filter: filterValue });

        // Call aosInit if available
        if (typeof aosInit === "function") {
          aosInit();
        }

        // Process HTMX attributes after filtering
        setTimeout(() => {
          if (typeof htmx !== "undefined") {
            const container = document.getElementById("categoryItemsContainer");
            htmx.process(container);
          }
          initializeGLightbox();
        }, 400);
      }
    });
  });
}

function initializeGLightbox() {
  // Destroy previous instance
  if (glightboxInstance && typeof glightboxInstance.destroy === "function") {
    glightboxInstance.destroy();
    glightboxInstance = null;
  }

  // Check if GLightbox is available
  if (typeof GLightbox === "undefined") {
    console.error("GLightbox is not loaded");
    return;
  }

  // Build gallery data based on current filter
  const galleryData = buildGalleryData();

  if (galleryData.length === 0) {
    console.log("No items to display in lightbox");
    return;
  }

  // Initialize GLightbox with gallery data
  glightboxInstance = GLightbox({
    elements: galleryData,
    touchNavigation: true,
    loop: true,
    autoplayVideos: true,
    skin: "clean",
    closeButton: true,
    touchFollowAxis: true,
    keyboardNavigation: true,
  });

  // Attach click events to portfolio lightbox links
  attachLightboxEvents();
}

function buildGalleryData() {
  let itemsToShow = [];

  if (portfolioData.currentFilter === "*") {
    // Show all items
    itemsToShow = portfolioData.items;
  } else {
    // Show items from specific category
    const categoryId = portfolioData.currentFilter.replace(
      ".filter-category-",
      ""
    );
    itemsToShow = portfolioData.items.filter(
      (item) => item.category_id.toString() === categoryId
    );
  }

  return itemsToShow.map((item, index) => {
    const mainImage =
      item.main_image || "/lib/static/core/img/placeholder-img.png";
    return {
      href: mainImage,
      type: "image",
      title: item.name,
      description: `${item.category_name} - ${item.name}`,
      alt: item.name,
    };
  });
}

function attachLightboxEvents() {
  const lightboxLinks = document.querySelectorAll(".portfolio-lightbox");

  lightboxLinks.forEach((link, index) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();

      const categoryId = this.getAttribute("data-category");
      const itemId = this.getAttribute("data-item-id");

      // Find the index of this item in the current gallery
      let startIndex = 0;
      const currentGallery = buildGalleryData();

      if (portfolioData.currentFilter === "*") {
        // Find index in all items
        startIndex = portfolioData.items.findIndex(
          (item) => item.id.toString() === itemId
        );
      } else {
        // Find index in filtered category items
        const filteredItems = portfolioData.items.filter(
          (item) => item.category_id.toString() === categoryId
        );
        startIndex = filteredItems.findIndex(
          (item) => item.id.toString() === itemId
        );
      }

      // Open lightbox at the correct index
      if (glightboxInstance && startIndex >= 0) {
        glightboxInstance.openAt(startIndex);
      }
    });
  });
}

// Utility function to check if an element is visible
function isElementVisible(element) {
  const style = getComputedStyle(element);
  return (
    style.display !== "none" &&
    style.visibility !== "hidden" &&
    style.opacity !== "0" &&
    !element.classList.contains("d-none")
  );
}

// Public API
window.portfolioFunctions = {
  refresh: initializePortfolio,

  filterByCategory(categoryId) {
    const filterValue =
      categoryId === "all" ? "*" : `.filter-category-${categoryId}`;
    portfolioData.currentFilter = filterValue;

    const buttons = document.querySelectorAll(
      ".isotope-filters li, .portfolio-filters li"
    );
    buttons.forEach((b) => b.classList.remove("filter-active"));

    const target = document.querySelector(`[data-filter="${filterValue}"]`);
    if (target) target.classList.add("filter-active");

    if (portfolioData.isotopeInstance) {
      portfolioData.isotopeInstance.arrange({ filter: filterValue });

      // Call aosInit if available
      if (typeof aosInit === "function") {
        aosInit();
      }

      setTimeout(() => {
        initializeGLightbox();
      }, 400);
    }
  },

  // Method to manually trigger lightbox reinitialization
  reinitializeLightbox() {
    initializeGLightbox();
  },

  // Get current portfolio state
  getState() {
    return {
      currentFilter: portfolioData.currentFilter,
      totalItems: portfolioData.items.length,
      totalCategories: portfolioData.categories.length,
      isotopeReady: !!portfolioData.isotopeInstance,
      lightboxReady: !!glightboxInstance,
    };
  },
};
