/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}"],
  theme: {
    extend: {
      animation: {
        'pulse-slow': 'pulse 6s linear infinite',
      }
    },
  },
  plugins: [],
}

