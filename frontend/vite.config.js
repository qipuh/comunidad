import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'node:url'

export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => tag.startsWith('ion-')
        }
      }
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      'vue': 'vue/dist/vue.esm-bundler.js'
    }
  },
  server: {
    middlewareMode: false,
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: ['comunidad.test', '.comunidad.test', 'localhost'],
    hmr: {
      host: 'localhost',
      port: 5173,
      protocol: 'ws'
    },
    proxy: {
      '/api': {
        target: 'https://comunidadcampesinatpct.com',
        changeOrigin: true,
        secure: true,
        rewrite: (path) => path
      },
      '/uploads': {
        target: 'https://comunidadcampesinatpct.com',
        changeOrigin: true,
        secure: true,
        rewrite: (path) => path
      }
    }
  }
})
