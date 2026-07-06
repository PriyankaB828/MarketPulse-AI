/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Inter', 'sans-serif'],
        outfit: ['Outfit', 'sans-serif'],
      },
      colors: {
        brand: {
          dark: '#070a13',
          card: '#0e1424',
          accent: '#00f2fe',
          glow: '#4facfe',
          success: '#00e676',
          warning: '#ffb300',
          danger: '#ff1744',
        }
      },
      boxShadow: {
        glow: '0 0 15px rgba(0, 242, 254, 0.35)',
        'glow-green': '0 0 15px rgba(0, 230, 118, 0.35)',
        'glow-red': '0 0 15px rgba(255, 23, 68, 0.35)',
      }
    },
  },
  plugins: [],
}
