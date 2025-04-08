import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import basicSsl from '@vitejs/plugin-basic-ssl'
import path from 'path'

export default defineConfig({
  plugins: [
    vue(),
    basicSsl()
  ],
  server: {
    port: 3001,
    https: true,
    host: true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      'three': 'three'
    }
  },
  optimizeDeps: {
    include: ['three', 'aframe'],
    exclude: ['@ar-js-org/ar.js']
  }
})