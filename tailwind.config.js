/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "jit",
  content: ["./templates/**/*.{html,htm}"],
  theme: {
    extend: {
      screens: {
        "m-s": "320px",
        "m-m": "375px",
        "m-l": "425px",
      },
    },
  },
  plugins: [],
};
