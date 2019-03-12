const pkg = require('./package')


module.exports = {
  mode: 'universal',

  /*
  ** Headers of the page
  */
  head: {
    title: pkg.name,
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: pkg.description }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      { rel: 'stylesheet', type: 'text/css', href: '//cdn.materialdesignicons.com/2.0.46/css/materialdesignicons.min.css' },
      { rel: 'stylesheet', type: 'text/css', href: 'https://fonts.googleapis.com/css?family=Raleway&Open+Sans' }
    ]
  },

  router: {
    middleware: 'router-auth'
  },

  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },

  /*
  ** Global CSS
  */
  css: [
    '@/assets/sass/style.sass'
  ],

  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    '@/plugins/vue-cookies.js'
  ],

  /*
  ** Nuxt.js modules
  */
  modules: [,
    // Doc:https://github.com/nuxt-community/modules/tree/master/packages/bulma
    // '@nuxtjs/bulma'
    '@nuxtjs/axios',
  ],

  env: {
    baseUrl: process.env.BASE_URL || 'http://localhost:9000'
  },

  axios: {
    // proxyHeaders: false
  },

  /*
  ** Build configuration
  */
  build: {
    vendor: ['axios', 'vue-cookies'],
    postcss: {
      preset: {
        features: {
          customProperties: false
        }
      }
    },
    /*
    ** You can extend webpack config here
    */
    extend(config, ctx) {
      
    }
  }
}
