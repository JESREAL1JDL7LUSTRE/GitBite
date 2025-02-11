import { Button } from "@/components/ui/button";
import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";
import { LogInIcon } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function SignInAndSignUp() {
  const navigate = useNavigate();

  return (
    <div className="p-2">
      <SignedOut>
        <div onClick={() => navigate('/')}>
          <SignInButton>
            <Button variant="outline" size="icon" className="w-full p-1">
              <LogInIcon/> Sign In
              </Button>
          </SignInButton>
        </div>
      </SignedOut>
      <SignedIn>
        <UserButton />
      </SignedIn>
    </div>
  );
}
