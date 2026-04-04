/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        'sol-purple': '#9945FF',
        'sol-green': '#14F195',
        'sol-blue': '#00D1FF',
        'dark': '#0a0a0f',
        'dark-card': '#111118',
        'dark-border': '#1e1e2e',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px #9945FF, 0 0 10px #9945FF' },
          '100%': { boxShadow: '0 0 20px #14F195, 0 0 30px #14F195' },
        },
      },
    },
  },
  plugins: [],
}
