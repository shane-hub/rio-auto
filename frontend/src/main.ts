// @ts-ignore
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
// @ts-ignore
import router from './router'
// @ts-ignore
import i18n from './i18n'
// @ts-ignore
import { createPinia } from 'pinia'
// @ts-ignore
import ElementPlus from 'element-plus'
// @ts-ignore
import 'element-plus/dist/index.css'
// @ts-ignore
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(i18n)
app.use(ElementPlus)

app.mount('#app')
