import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/build-a-next-gen-inventory-management-system-the-app-must-be-secured-by-a-beauti-de2663/",
  build: { outDir: "dist", assetsDir: "assets" },
  server: { port: 3000 },
});
