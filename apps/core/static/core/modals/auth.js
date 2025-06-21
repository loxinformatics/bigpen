const overlayHeading = document.querySelector("#loginSignupModal .overlay-heading")
const overlayParagraph = document.querySelector("#loginSignupModal .overlay-paragraph")
const signInLink = document.querySelector("#loginSignupModal .signin-link")
const signUpLink = document.querySelector("#loginSignupModal .signup-link")


// Function to update the login-signup-modal heading and paragraph based on available components
function updateOverlayHeadingParagraph() {
  if (!overlayHeading && !overlayParagraph) return;

  const hasSignIn = !!signInLink;
  const hasSignUp = !!signUpLink

  let headingText = "";
  let paragraphText = "";

  if (hasSignIn && hasSignUp) {
    headingText = "Add to Cart"
    paragraphText = "Please sign in to your account or create a new one.";
  } else if (hasSignUp && !hasSignIn) {
    headingText = "Add to Cart";
    paragraphText = "Please create an account to continue.";
  } else if (hasSignIn && !hasSignUp) {
    headingText = "Add to Cart";
    paragraphText = "Please sign in to continue.";
  } else {
    // If neither component is available, hide the heading and paragraph

    overlayHeading.style.display = 'none';
    overlayParagraph.style.display = 'none';
    return;
  }

  overlayHeading.textContent = headingText;
  overlayHeading.style.display = 'block';

  overlayParagraph.textContent = paragraphText;
  overlayParagraph.style.display = 'block';
}

// Run the function immediately since script is deferred
updateOverlayHeadingParagraph();