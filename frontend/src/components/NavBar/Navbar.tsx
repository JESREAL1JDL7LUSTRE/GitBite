import { Link, useNavigate } from "react-router-dom";
import logo from '@/assets/logo.png'
import { ModeToggle } from "../ui/mode-toggle";
LucideImport
  import { LucideImport, ShoppingCart } from "lucide-react";
import { Button } from "../ui/button";
import { Item } from "@radix-ui/react-dropdown-menu";
import { NavMenu } from "./NavMenu";

export default function Navbar() {
  const nav = useNavigate()
  return (
    <>
      <nav>
        <div className="container flex justify-between items-center py-2">
          <div className="flex items-center gap-1 font-bold">
        <Link to='/' className='nav-logo'>
          <img src={logo} alt='logo' width={50} />
        </Link>
        <p>BrandName</p>
          </div>
          <div className="flex items-center gap-4">
        <div className="hidden md:block">
          <ul>
            <NavMenu />
          </ul>
        </div>
        <Button onClick={() => { nav('cart') }}><ShoppingCart /></Button>
        <Button onClick={() => { nav('login') }}>Login</Button>
        <ModeToggle />
          </div>
        </div>
      </nav>
          
    </>
  
  )
}
