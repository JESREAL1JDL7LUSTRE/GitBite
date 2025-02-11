import { Link } from "react-router-dom";
import SignInAndSignUp from "./SignInAndSignUp";

export default function Navbar() {
  return (
    <div className=" fixed top-0 left-0 w-full bg-red-500 p-1 shadow-lg z-50 h-16">
      <div className="flex items-center justify-between">
        <Link to="/" className="text-xl font-bold font-mono tracking-wider">
          GitBite
        </Link>

        <div>
          <SignInAndSignUp />
        </div>
      </div>
    </div>
  );
}
