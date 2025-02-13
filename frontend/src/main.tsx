import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Recipes from "./pages/Recipes.tsx";
import About from "./pages/About.tsx";
import Cart from "./pages/Cart.tsx";
import Authors from "./pages/Authors.tsx";
import Food from "./pages/Categories/Food.tsx";
import Drinks from "./pages/Categories/Drinks.tsx";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { path: "recipes", element: <Recipes /> },
      { path: "authors", element: <Authors /> },
      { path: "about", element: <About /> },
      { path: "cart", element: <Cart /> },
      { path: "food", element: <Food /> },
      { path: "drinks", element: <Drinks /> },
    ],
  },
]);

createRoot(document.getElementById("root")!).render(
    <RouterProvider router={router} />
);