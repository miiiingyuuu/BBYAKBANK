import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import BootstrapVue3 from 'bootstrap-vue-3'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
import '@fortawesome/fontawesome-free/css/all.css'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import { ko } from 'vuetify/locale'

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const vuetify = createVuetify({
  components,
  directives,
  locale: {
    locale: 'ko',
    messages: { ko }
  }
})

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)
app.use(BootstrapVue3)
app.use(pinia)
app.use(router)
app.use(vuetify)



app.mount('#app')
