// Toggle logic for the mobile menu
const menuBtn = document.getElementById("mobile-menu-toggle");
const menu = document.getElementById("mobile-menu");
const icon = document.getElementById("hamburger-icon");

menuBtn.addEventListener("click", () => {
  const isHidden = menu.classList.toggle("hidden");
  // Switch icon between Hamburger and X
  icon.setAttribute(
    "d",
    isHidden ? "M4 6h16M4 12h16M4 18h16" : "M6 18L18 6M6 6l12 12",
  );
});

document.body.addEventListener("htmx:configRequest", (event) => {
  event.detail.headers["X-CSRFToken"] = "{{ csrf_token }}";
});
