import path from "path";
import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

// Load environment variables
export default defineConfig(({ mode }) => {
  // Load the correct `.env` file
  const env = loadEnv(mode, process.cwd(), "");

  return {
    plugins: [react()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    define: {
      "import.meta.env.VITE_CLERK_FRONTEND_API_URL": JSON.stringify(
        env.VITE_CLERK_FRONTEND_API_URL
      ),
    },
  };
});
