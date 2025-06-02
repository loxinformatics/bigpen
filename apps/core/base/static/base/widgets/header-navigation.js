/**
 * Apply .active class on Navlinks based on the current URL.
 */
function setActiveHeaderNavLink() {
  const currentUrl = window.location.pathname;
  const navLinks = document.querySelectorAll('.header-navlink');

  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentUrl) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
}
setActiveHeaderNavLink(); 
