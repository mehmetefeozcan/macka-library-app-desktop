/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "jit",
  content: ["./templates/**/*.{html,htm}"],
  theme: {
    extend: {
      fontFamily: {
        'dancing-scripts' : ['"Dancing Scripts"', 'cursive'],
        'rubik' : ['"Rubik"', 'cursive'],
      },
      screens: {
        "m-s": "320px",
        "m-m": "375px",
        "m-l": "425px",
      },
    },
  },
  plugins: [],
};
