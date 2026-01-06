/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      '.hbcats/cats/templates/**/*.html',
      '.hbcats/**/templates/**/*.html',
      '.hbcats/static/cats/js/*.js',
      '.hbcats/cats/static/cats/js/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
