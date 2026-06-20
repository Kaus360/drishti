/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0a0f1e',
        primary: '#f97316',
        secondary: '#06b6d4',
      },
    },
  },
  plugins: [],
}
