import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f0ff',
          100: '#e0e0ff',
          200: '#c800ff',
          300: '#b700ff',
          400: '#a600ff',
          500: '#9500ff',
          600: '#8400ff',
          700: '#7300ff',
          800: '#6200ff',
          900: '#5100ff',
        },
        success: '#39ff14',
        warning: '#ffff00',
        danger: '#ff006e',
        info: '#00ffff',
        neon: {
          pink: '#ff006e',
          green: '#39ff14',
          blue: '#0099ff',
          purple: '#9500ff',
          cyan: '#00ffff',
          yellow: '#ffff00',
        },
      },
    },
  },
  plugins: [],
};

export default config;
