const sectionParagraph = document.querySelector('#contact .section-title p');
const contactFormContainer = document.querySelector('#contact .contact-form-container');
const contactInfoContainer = document.querySelector('#contact .contact-info-container');

// Function to update the contact section paragraph based on available components
function updateContactParagraph() {
  if (!sectionParagraph) return;

  const hasContactForm = contactFormContainer && contactFormContainer.offsetParent !== null;
  const hasContactInfo = contactInfoContainer && contactInfoContainer.offsetParent !== null;

  let paragraphText = '';

  if (hasContactForm && hasContactInfo) {
    paragraphText = "If you have an inquiry, you can get in touch with us using the information below, or you can fill the form and we'll get back to you.";
  } else if (hasContactInfo && !hasContactForm) {
    paragraphText = "If you have an inquiry, you can get in touch with us using the information below.";
  } else if (hasContactForm && !hasContactInfo) {
    paragraphText = "If you have an inquiry, you can fill the form and we'll get back to you.";
  } else {
    // If neither component is available, hide the paragraph
    sectionParagraph.style.display = 'none';
    return;
  }

  sectionParagraph.textContent = paragraphText;
  sectionParagraph.style.display = 'block';
}

// Run the function immediately since script is deferred
updateContactParagraph();