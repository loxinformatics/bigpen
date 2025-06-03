/**
 * Whatsapp button
 */
let whatsappBtn = document.querySelector('.whatsapp-button');

function toggleWhatsappBtn() {
  if (whatsappBtn) {
    window.scrollY > 100 ? whatsappBtn.classList.add('active') : whatsappBtn.classList.remove('active');
  }
}

window.addEventListener('load', toggleWhatsappBtn);
document.addEventListener('scroll', toggleWhatsappBtn);

/**
 * Call Float
 */
let callFloat = document.querySelector('.call-float');

function toggleCallFloat() {
  if (callFloat) {
    window.scrollY > 100 ? callFloat.classList.add('active') : callFloat.classList.remove('active');
  }
}

window.addEventListener('load', toggleCallFloat);
document.addEventListener('scroll', toggleCallFloat);