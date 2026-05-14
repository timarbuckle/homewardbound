/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Look for any HTML file in the root templates directory
    "./templates/**/*.html",
    // Look for any HTML file inside any app directory
    "./**/templates/**/*.html",
    // Look for classes inside Python files (tags/filters/forms)
    "./**/forms.py",
    "./**/tables.py",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
