const asideElement = document.getElementById("aside");
const mediaQuery = window.matchMedia("(min-width: 1200px)");

/* ───── Call Float ───── */
const callFloat = document.querySelector(".call-float");

function toggleCallFloat() {
  if (callFloat) {
    callFloat.classList.toggle("active", window.scrollY > 100);
  }
}

function updateCallFloatLeftValue() {
  if (!callFloat) return;
  // Shift if screen is wide (desktop), otherwise hug the edge
  callFloat.style.left = mediaQuery.matches ? "316px" : "1rem";
}

/* ───── Whatsapp Float ───── */
const whatsappFloat = document.querySelector(".whatsapp-float");

function toggleWhatsappFloat() {
  if (whatsappFloat) {
    whatsappFloat.classList.toggle("active", window.scrollY > 100);
  }
}

function updateWhatsAppFloatLeftValue() {
  if (!whatsappFloat) return;
  // Shift if screen is wide (desktop), otherwise hug the edge
  whatsappFloat.style.left = mediaQuery.matches ? "316px" : "1rem";
}

/* ───── Initial Setup ───── */
toggleCallFloat();
toggleWhatsappFloat();
updateCallFloatLeftValue();
updateWhatsAppFloatLeftValue();

/* ───── Listeners ───── */
document.addEventListener("scroll", () => {
  toggleCallFloat();
  toggleWhatsappFloat();
});

mediaQuery.addEventListener("change", () => {
  updateCallFloatLeftValue();
  updateWhatsAppFloatLeftValue();
});
