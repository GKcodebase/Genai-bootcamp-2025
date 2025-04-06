import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/styles.css'

// Import AR dependencies after Vue is initialized
window.addEventListener('load', () => {
  import('aframe').then(() => {
    import('@ar-js-org/ar.js/aframe/build/aframe-ar').then(() => {
      console.log('AR dependencies loaded');
    });
  });
});

const app = createApp(App)
app.use(router)
app.mount('#app')

// For debugging
console.log('Vue app initialized')