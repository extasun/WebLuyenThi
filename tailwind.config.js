/** @type {import('tailwindcss').Config} */
module.exports = {
  mode : 'jit',
  content: ['./templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ],
  
  theme: {
    extend: {
      height: {
        '128': '28rem', 
        '200': '50rem',  
        '400': '100rem',
      },
      width: {
        '128': '40rem', 
      }
    },
  },
  plugins: [
    require('flowbite/plugin')
]
}

