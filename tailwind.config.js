/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      '.hbcats/cats/templates/**/*.html',
      './**/templates/**/*.html',
      '.hbcats/**/templates/**/*.html',
      '.hbcats/cats/static/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
