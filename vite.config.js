import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
  },
  publicDir: 'public',  // This was missing in my previous response
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: true,
  }
});