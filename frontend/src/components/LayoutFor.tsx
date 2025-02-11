import { Outlet } from "react-router-dom";
import Navbar from "./NavBar/Navbar";

const LayoutFor: React.FC = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-grow pt-16">
        <Outlet />
      </main>
    </div>
  );
};

export default LayoutFor;
