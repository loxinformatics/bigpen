

// *************************** HEADER *************************



/**
 * Init isotope layout and filters
 */
document.querySelectorAll('.isotope-layout').forEach(function (isotopeItem) {
  let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
  let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
  let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

  let initIsotope;
  imagesLoaded(isotopeItem.querySelector('.isotope-container'), function () {
    initIsotope = new Isotope(isotopeItem.querySelector('.isotope-container'), {
      itemSelector: '.isotope-item',
      layoutMode: layout,
      filter: filter,
      sortBy: sort
    });
  });

  isotopeItem.querySelectorAll('.isotope-filters li').forEach(function (filters) {
    filters.addEventListener('click', function () {
      isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
      this.classList.add('filter-active');
      initIsotope.arrange({
        filter: this.getAttribute('data-filter')
      });
      if (typeof aosInit === 'function') {
        aosInit();
      }
    }, false);
  });

});



/**
 * Ecommerce Cart Functionality
 * Handles quantity changes and item removal
 */

function ecommerceCartTools() {
  // Get all quantity buttons and inputs directly
  const decreaseButtons = document.querySelectorAll('.quantity-btn.decrease');
  const increaseButtons = document.querySelectorAll('.quantity-btn.increase');
  const quantityInputs = document.querySelectorAll('.quantity-input');
  const removeButtons = document.querySelectorAll('.remove-item');

  // Decrease quantity buttons
  decreaseButtons.forEach(btn => {
    btn.addEventListener('click', function () {
      const quantityInput = btn.closest('.quantity-selector').querySelector('.quantity-input');
      let currentValue = parseInt(quantityInput.value);
      if (currentValue > 1) {
        quantityInput.value = currentValue - 1;
      }
    });
  });

  // Increase quantity buttons
  increaseButtons.forEach(btn => {
    btn.addEventListener('click', function () {
      const quantityInput = btn.closest('.quantity-selector').querySelector('.quantity-input');
      let currentValue = parseInt(quantityInput.value);
      if (currentValue < parseInt(quantityInput.getAttribute('max'))) {
        quantityInput.value = currentValue + 1;
      }
    });
  });

  // Manual quantity inputs
  quantityInputs.forEach(input => {
    input.addEventListener('change', function () {
      let currentValue = parseInt(input.value);
      const min = parseInt(input.getAttribute('min'));
      const max = parseInt(input.getAttribute('max'));

      // Validate input
      if (isNaN(currentValue) || currentValue < min) {
        input.value = min;
      } else if (currentValue > max) {
        input.value = max;
      }
    });
  });

  // Remove item buttons
  removeButtons.forEach(btn => {
    btn.addEventListener('click', function () {
      btn.closest('.cart-item').remove();
    });
  });
}

ecommerceCartTools();
