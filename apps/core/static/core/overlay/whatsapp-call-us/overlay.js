const asideElement = document.getElementById("aside");
const mediaQuery = window.matchMedia("(min-width: 1200px)");

/* ───── Call Float ───── */
const callFloat = document.querySelector(".call-float");

function updateCallFloatLeftValue() {
  if (!callFloat) return;
  // Shift if screen is wide (desktop), otherwise hug the edge
  callFloat.style.left = mediaQuery.matches ? "316px" : "1rem";
}

/* ───── Whatsapp Float ───── */
const whatsappFloat = document.querySelector(".whatsapp-float");

function updateWhatsAppFloatLeftValue() {
  if (!whatsappFloat) return;
  // Shift if screen is wide (desktop), otherwise hug the edge
  whatsappFloat.style.left = mediaQuery.matches ? "316px" : "1rem";
}

/* ───── Initial Setup ───── */
updateCallFloatLeftValue();
updateWhatsAppFloatLeftValue();

/* ───── Listeners ───── */
mediaQuery.addEventListener("change", () => {
  updateCallFloatLeftValue();
  updateWhatsAppFloatLeftValue();
});
