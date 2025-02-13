import { Link } from "react-router-dom";
import logo from '@/assets/logo.png'
import SignInAndSignUp from "./SignInAndSignUp";
import { ModeToggle } from "../ui/mode-toggle";
LucideImport
  import { LucideImport, ShoppingBasket, ShoppingCart } from "lucide-react";
export default function Navbar() {
  return (
  <nav>
    <div id="container" className="fixed top-0 left-0 border-b-2 border-gray-500 bg-white-500 flex w-full p-1">
        <Link to='/' className='nav-logo flex items-center ml-2'>
          <img src={logo} alt='logo' width={50} />
        </Link>
        <div></div>
        <ul className='nav-menu flex items-center justify-center w-full flex-grow space-x-5 '>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/Menu">Menu</Link>
          </li>
          <div>
            <ShoppingCart />
          </div>
          <div>
            <SignInAndSignUp />
          </div>
          <div> 
            <ModeToggle />
          </div>
          
        </ul>    
    </div>
  </nav>
  )
}
