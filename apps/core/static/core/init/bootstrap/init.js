/**
 * Apply .scrolled class to the body as the page is scrolled down
 */
function toggleScrolled() {
  const selectBody = document.querySelector('body');
  const selectHeader = document.querySelector('#header');
  if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
  window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
}

document.addEventListener('scroll', toggleScrolled);
window.addEventListener('load', toggleScrolled);

/**
 * Correct scrolling position upon page load for URLs containing hash links.
 */
window.addEventListener('load', function (e) {
  if (window.location.hash) {
    if (document.querySelector(window.location.hash)) {
      setTimeout(() => {
        let section = document.querySelector(window.location.hash);
        let scrollMarginTop = getComputedStyle(section).scrollMarginTop;
        window.scrollTo({
          top: section.offsetTop - parseInt(scrollMarginTop),
          behavior: 'smooth'
        });
      }, 100);
    }
  }
});

/**
 * Apply .active class on Navlinks based on the current URL.
 */
function setActiveNavLink() {
  const currentUrl = window.location.pathname;
  const navLinks = document.querySelectorAll('.navlink');

  navLinks.forEach(link => {
    const linkPath = new URL(link.href, window.location.origin).pathname;

    if (linkPath === currentUrl) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}

document.addEventListener('DOMContentLoaded', setActiveNavLink);
