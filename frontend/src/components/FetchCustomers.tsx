import { useEffect, useState } from "react";

interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
}

const fetchUser = async (): Promise<User | null> => {
  try {
    const response = await fetch("https://your-ngrok-url/api/customers/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
      },
    });

    if (!response.ok) throw new Error("Failed to fetch user data");

    const userData: User = await response.json();
    console.log("User Data:", userData);
    return userData;
  } catch (error) {
    console.error("Error fetching user:", error);
    return null;
  }
};

const Profile = () => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    fetchUser().then(setUser);
  }, []);

  if (!user) return <p>Loading user data...</p>;

  return (
    <div>
      <h1>Welcome, {user.first_name} {user.last_name}</h1>
      <p>Email: {user.email}</p>
    </div>
  );
};

export default Profile;
