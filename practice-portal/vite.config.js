import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "/practice/",
  plugins: [react()],
  server: { port: 5173 },
  build: {
    outDir: "../frontend/practice",
    emptyOutDir: true,
  },
});
