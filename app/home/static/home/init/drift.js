/**
 * Product Image Zoom and Thumbnail Functionality
 */

function productDetailFeatures() {
  // Initialize Drift for image zoom
  function initDriftZoom() {
    // Check if Drift is available
    if (typeof Drift === 'undefined') {
      console.error('Drift library is not loaded');
      return;
    }

    const driftOptions = {
      paneContainer: document.querySelector('.image-zoom-container'),
      inlinePane: window.innerWidth < 768 ? true : false,
      inlineOffsetY: -85,
      containInline: true,
      hoverBoundingBox: false,
      zoomFactor: 3,
      handleTouch: false
    };

    // Initialize Drift on the main product image
    const mainImage = document.getElementById('main-product-image');
    if (mainImage) {
      new Drift(mainImage, driftOptions);
    }
  }

  // Thumbnail click functionality
  function initThumbnailClick() {
    const thumbnails = document.querySelectorAll('.thumbnail-item');
    const mainImage = document.getElementById('main-product-image');

    if (!thumbnails.length || !mainImage) return;

    thumbnails.forEach(thumbnail => {
      thumbnail.addEventListener('click', function () {
        // Get image path from data attribute
        const imageSrc = this.getAttribute('data-image');

        // Update main image src and zoom attribute
        mainImage.src = imageSrc;
        mainImage.setAttribute('data-zoom', imageSrc);

        // Update active state
        thumbnails.forEach(item => item.classList.remove('active'));
        this.classList.add('active');

        // Reinitialize Drift for the new image
        initDriftZoom();
      });
    });
  }

  // Image navigation functionality (prev/next buttons)
  function initImageNavigation() {
    const prevButton = document.querySelector('.image-nav-btn.prev-image');
    const nextButton = document.querySelector('.image-nav-btn.next-image');

    if (!prevButton || !nextButton) return;

    const thumbnails = Array.from(document.querySelectorAll('.thumbnail-item'));
    if (!thumbnails.length) return;

    // Function to navigate to previous or next image
    function navigateImage(direction) {
      // Find the currently active thumbnail
      const activeIndex = thumbnails.findIndex(thumb => thumb.classList.contains('active'));
      if (activeIndex === -1) return;

      let newIndex;
      if (direction === 'prev') {
        // Go to previous image or loop to the last one
        newIndex = activeIndex === 0 ? thumbnails.length - 1 : activeIndex - 1;
      } else {
        // Go to next image or loop to the first one
        newIndex = activeIndex === thumbnails.length - 1 ? 0 : activeIndex + 1;
      }

      // Simulate click on the new thumbnail
      thumbnails[newIndex].click();
    }

    // Add event listeners to navigation buttons
    prevButton.addEventListener('click', () => navigateImage('prev'));
    nextButton.addEventListener('click', () => navigateImage('next'));
  }

  // Initialize all features
  initDriftZoom();
  initThumbnailClick();
  initImageNavigation();
}

productDetailFeatures();
