/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Look for any HTML file in the root templates directory
    "./hbcats/cats/templates/**/*.html",
    // Look for any HTML file inside any app directory
    "./**/templates/**/*.html",
    // Look for classes inside Python files (tags/filters/forms)
    "./hbcats/cats/*.py",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
