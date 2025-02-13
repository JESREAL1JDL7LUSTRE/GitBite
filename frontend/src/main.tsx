import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ClerkProvider } from "@clerk/clerk-react";
import Item from "./pages/Item.tsx";
import LayoutFor from "./components/LayoutFor.tsx";

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;
const FRONTEND_API = import.meta.env.VITE_CLERK_FRONTEND_API_URL;

if (!FRONTEND_API) {
  throw new Error("❌ Missing VITE_CLERK_FRONTEND_API_URL in .env");
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <LayoutFor />,
    children: [
      { index: true, element: <App /> },
      { path: "item", element: <Item /> },
    ],
  },
]);

createRoot(document.getElementById("root")!).render(
  <ClerkProvider publishableKey={PUBLISHABLE_KEY} afterSignOutUrl={"/"}>
    <RouterProvider router={router} />
  </ClerkProvider>
);
