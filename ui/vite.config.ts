import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/stats": { target: "http://localhost:8000" },
      "/process-survey": { target: "http://localhost:8000" },
    },
  },
});
