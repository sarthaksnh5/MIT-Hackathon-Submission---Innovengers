/** @type {import('tailwindcss').Config} */
module.exports = {
  // NOTE: Update this to include the paths to all of your component files.
  content: ['./App.{js,jsx,ts,tsx}', './src/**/*.{js,jsx,ts,tsx,css}'],
  presets: [require('nativewind/preset')],
  theme: {
    extend: {
      colors: {
        theme: '#14B8A6',
        'light-theme': '#14b8a680',
        'dark-theme': '#03574e',
        'blue-gray': '#0f172a',
      },
      spacing: {
        '8xl': '96rem',
        '9xl': '128rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
      fontFamily: {
        sans: ['Nunito'], // Only Nunito, no fallback fonts
      },
      keyframes: {
        pan: {
          '0%': {'background-position': '100% 50%'},
          '100%': {'background-position': '0% 50%'},
        },
      },
      animation: {
        pan: 'pan 15s linear infinite',
      },
    },
  },
  plugins: [],
};
