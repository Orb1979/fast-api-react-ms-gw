import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,

    // proxy: {
    //   '/api/': {
    //     target: 'http://localhost:8081',
    //     changeOrigin: true
    //   }
    // }

    //Test through Nginx Gateway
    proxy: {
      '/api/': {
        target: 'http://localhost:80',
        changeOrigin: true
      }
    }

  }
});

/*
1. Browser
   → GET http://localhost:5173/api/xxx

2. Vite dev server (5173)
   → sees '/api/' match
   → proxies request

3. Vite sends NEW request:
   → http://localhost:80/api/xxx

4. Nginx (port 80)
   → receives it
   → routes to backend

5. Response goes back:
   Backend → Nginx → Vite → Browser
 */