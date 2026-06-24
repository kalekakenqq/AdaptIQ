/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0f172a",
        card: "#1e293b",
        accent: {
          DEFAULT: "#6366f1",
          light: "#818cf8",
        },
        text: {
          DEFAULT: "#f1f5f9",
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};
