// Think of a class like a recipe book for making portfolios
// This class contains all the instructions for creating and managing a portfolio
class PortfolioManager {
  // The constructor is like the "preparation" section of a recipe
  // It sets up all our ingredients (data) before we start cooking
  constructor() {
    // These are our "ingredients" - stored in the class using 'this'
    // 'this' means "this specific portfolio we're making"
    this.categories = []; // List to hold all portfolio categories
    this.items = []; // List to hold all portfolio items
    this.currentFilter = "*"; // Which filter is currently active (* means "show all")
    this.apiBaseUrl = "/api"; // Where our server lives
    this.isotopeInstance = null; // Will hold our fancy grid layout system

    // Start the cooking process as soon as our ingredients are ready
    this.init();
  }

  // This method waits for the webpage to be completely ready
  // Like waiting for the oven to preheat before baking
  init() {
    document.addEventListener("DOMContentLoaded", () => {
      // Wait just a tiny bit more to make sure everything is really ready
      // Like letting bread dough rest before baking
      setTimeout(() => {
        this.initializePortfolio();
      }, 100);
    });
  }

  // This is our main "cooking" method - it does everything in the right order
  // Like following a recipe step by step
  async initializePortfolio() {
    try {
      // Do these steps one at a time, waiting for each to finish
      await this.loadPortfolioCategories(); // Step 1: Get the categories
      await this.loadPortfolioItems(); // Step 2: Get the items for each category
      this.renderPortfolioFilters(); // Step 3: Create the filter buttons
      this.renderPortfolioItems(); // Step 4: Display all the items
      this.attachPortfolioEventListeners(); // Step 5: Make the buttons work
    } catch (error) {
      // If something goes wrong, tell us what happened
      console.error("Error initializing portfolio:", error);
    }
  }

  // This method asks the server "What categories do you have?"
  // Like asking a librarian "What sections do you have in your library?"
  async loadPortfolioCategories() {
    try {
      // Send a request to our server
      const response = await fetch(
        `${this.apiBaseUrl}/portfolio/?is_active=true`
      );

      // Check if the server responded nicely
      if (!response.ok) {
        throw new Error("Failed to load categories");
      }

      // Convert the server's response into JavaScript objects we can use
      this.categories = await response.json();
    } catch (error) {
      // If something went wrong, log it and use an empty list
      console.error("Error loading categories:", error);
      this.categories = [];
    }
  }

  // This method gets all the items for each category
  // Like asking "Show me all the books in each section of the library"
  async loadPortfolioItems() {
    try {
      // For each category, ask the server for its items
      // We use map() to create a list of promises (like a list of questions we're asking)
      const itemPromises = this.categories.map(async (category) => {
        // Ask the server for items in this specific category
        const response = await fetch(
          `${this.apiBaseUrl}/portfolio/${category.id}/items/`
        );

        // Check if the server gave us a good response
        if (!response.ok) {
          throw new Error(`Failed to load items for category ${category.id}`);
        }

        const categoryItems = await response.json();

        // Add extra information to each item (which category it belongs to)
        // Like adding a library sticker to each book showing which section it's from
        return categoryItems.map((item) => ({
          ...item, // Keep all the original item information
          category_id: category.id, // Add the category ID
          category_name: category.name, // Add the category name
        }));
      });

      // Wait for all our questions to be answered
      const itemArrays = await Promise.all(itemPromises);

      // Combine all the arrays into one big list
      // Like putting all the books from all sections into one big pile
      this.items = itemArrays.flat();
    } catch (error) {
      console.error("Error loading items:", error);
      this.items = [];
    }
  }

  // This method creates the filter buttons at the top of the page
  // Like creating tabs to organize different types of photos in an album
  renderPortfolioFilters() {
    // Find where the filter buttons should go
    const filtersContainer = document.getElementById("categoryFilters");
    if (!filtersContainer) return; // If we can't find it, stop here

    // Create the "All Categories" button first
    const allFilter = document.createElement("li");
    allFilter.setAttribute("data-filter", "*"); // "*" means "show everything"
    allFilter.classList.add("filter-active"); // Make it look selected
    allFilter.innerHTML = '<i class="bi bi-grid me-2"></i>All Categories';

    // Clear out any old buttons and add our "All" button
    filtersContainer.innerHTML = "";
    filtersContainer.appendChild(allFilter);

    // Create a button for each category we have
    this.categories.forEach((category) => {
      const filter = document.createElement("li");
      // Set up the filter to show only items from this category
      filter.setAttribute("data-filter", `.filter-category-${category.id}`);
      filter.innerHTML = `<i class="${category.bootstrap_icon} me-2"></i>${category.name}`;
      filtersContainer.appendChild(filter);
    });
  }

  // This method puts all our portfolio items on the webpage
  // Like laying out all your photos on a table to look at them
  renderPortfolioItems() {
    // Find the container where items should be displayed
    const container = document.getElementById("categoryItemsContainer");
    if (!container) return; // If we can't find it, stop here

    // Clear out any old items first
    container.innerHTML = "";

    // Create and add each portfolio item to the page
    this.items.forEach((item) => {
      const element = this.createPortfolioItemElement(item);
      container.appendChild(element);
    });

    // Tell HTMX about our new content (if HTMX is available)
    // HTMX is a library that makes web pages more interactive
    if (typeof htmx !== "undefined") {
      htmx.process(container);
    }

    // Set up the fancy grid layout
    this.initializeIsotope(container);
  }

  // This method sets up Isotope - a library that makes pretty, responsive grids
  // Like having a magic system that automatically arranges your photos nicely
  initializeIsotope(container) {
    // If we already have an Isotope running, stop it first
    // Like clearing a table before setting up a new puzzle
    if (this.isotopeInstance) {
      this.isotopeInstance.destroy();
      this.isotopeInstance = null;
    }

    // Check if the Isotope library is available
    if (typeof Isotope === "undefined") {
      console.error("Isotope is not loaded");
      return;
    }

    // Get settings from the HTML or use sensible defaults
    const isotopeLayout = container.closest(".isotope-layout");
    let layout = isotopeLayout?.getAttribute("data-layout") ?? "masonry";
    let filter = isotopeLayout?.getAttribute("data-default-filter") ?? "*";
    let sort = isotopeLayout?.getAttribute("data-sort") ?? "original-order";

    // Wait a moment for images to load, then create our grid
    // Like waiting for paint to dry before hanging pictures
    setTimeout(() => {
      this.isotopeInstance = new Isotope(container, {
        itemSelector: ".isotope-item", // Which elements to arrange
        layoutMode: layout, // How to arrange them (like "masonry" - like a brick wall)
        filter: filter, // Which ones to show initially
        sortBy: sort, // What order to show them in
        percentPosition: true, // Use percentages for flexible positioning
        masonry: {
          // Settings for the brick-wall layout
          columnWidth: ".isotope-item",
          gutter: 0, // No gaps between items
        },
        transitionDuration: "0.4s", // How long animations take (smooth transitions)
      });
    }, 200);
  }

  // This method creates the HTML for one portfolio item
  // Like creating a frame with a photo, title, and description
  createPortfolioItemElement(item) {
    // Use the item's main image, or a placeholder if there's no image
    const mainImage =
      item.main_image || "/lib/static/core/img/placeholder-img.png";

    // Create the main container element
    const wrapper = document.createElement("div");
    wrapper.className = `col-lg-6 col-md-6 portfolio-item isotope-item filter-category-${item.category_id}`;

    // Fill the container with HTML content
    // This creates the visual layout for each portfolio item
    wrapper.innerHTML = `
      <div class="portfolio-wrap">
        <img src="${mainImage}" class="img-fluid" alt="${item.name}" loading="lazy">
        <div class="portfolio-info">
          <div class="content">
            <span class="category">${item.category_name}</span>
            <h4>${item.name}</h4>
            <div class="portfolio-links">
              <a href="#" 
                 class="portfolio-modal-toggle" 
                 title="${item.name}"
                 data-category="${item.category_id}"
                 data-item-id="${item.id}"
                 data-bs-toggle="modal" 
                 data-bs-target="#loginSignupModal">
                 <i class="bi bi-cart-plus"></i>
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

  // This method makes the filter buttons actually work when clicked
  // Like connecting the light switches to the lights
  attachPortfolioEventListeners() {
    // Find all the filter buttons on the page
    const filterButtons = document.querySelectorAll(
      ".isotope-filters li, .portfolio-filters li"
    );

    // For each button, add a "click listener" (like a doorbell that listens for rings)
    filterButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        // When a button is clicked:

        // 1. Remove the "active" look from all buttons
        filterButtons.forEach((f) => f.classList.remove("filter-active"));

        // 2. Make the clicked button look "active"
        btn.classList.add("filter-active");

        // 3. Find out which filter was clicked
        const filterValue = btn.getAttribute("data-filter");
        this.currentFilter = filterValue;

        // 4. Apply the filter to our grid (if Isotope is ready)
        if (this.isotopeInstance) {
          this.isotopeInstance.arrange({ filter: filterValue });

          // Refresh any animations that might be on the page
          if (typeof aosInit === "function") {
            aosInit();
          }

          // Tell HTMX about the newly filtered content
          setTimeout(() => {
            if (typeof htmx !== "undefined") {
              const container = document.getElementById(
                "categoryItemsContainer"
              );
              htmx.process(container);
            }
          }, 400);
        }
      });
    });
  }

  // Utility method to check if an element is visible on the page
  // Like checking if a photo is face-up or hidden under other photos
  isElementVisible(element) {
    const style = getComputedStyle(element);
    return (
      style.display !== "none" && // Not hidden with display
      style.visibility !== "hidden" && // Not hidden with visibility
      style.opacity !== "0" && // Not transparent
      !element.classList.contains("d-none") // Not hidden with Bootstrap class
    );
  }

  // Public method that other parts of the website can call to refresh everything
  // Like having a "restart" button
  refresh() {
    this.initializePortfolio();
  }

  // Public method to filter by a specific category
  // Like having a remote control to change the channel
  filterByCategory(categoryId) {
    // Figure out the filter value
    const filterValue =
      categoryId === "all" ? "*" : `.filter-category-${categoryId}`;
    this.currentFilter = filterValue;

    // Update the button appearance
    const buttons = document.querySelectorAll(
      ".isotope-filters li, .portfolio-filters li"
    );
    buttons.forEach((b) => b.classList.remove("filter-active"));

    // Find and highlight the correct button
    const target = document.querySelector(`[data-filter="${filterValue}"]`);
    if (target) target.classList.add("filter-active");

    // Apply the filter
    if (this.isotopeInstance) {
      this.isotopeInstance.arrange({ filter: filterValue });

      // Refresh animations if available
      if (typeof aosInit === "function") {
        aosInit();
      }
    }
  }

  // Public method to get information about the current state
  // Like asking "What's currently showing and how many items do we have?"
  getState() {
    return {
      currentFilter: this.currentFilter,
      totalItems: this.items.length,
      totalCategories: this.categories.length,
      isotopeReady: !!this.isotopeInstance, // !! converts to true/false
    };
  }
}

// Create our one and only portfolio manager
// This is like building a house from our blueprint
const portfolioManager = new PortfolioManager();

// Make some functions available to the rest of the website
// Like having a front door that visitors can use
window.portfolioFunctions = {
  refresh: () => portfolioManager.refresh(),
  filterByCategory: (categoryId) =>
    portfolioManager.filterByCategory(categoryId),
  getState: () => portfolioManager.getState(),
};
