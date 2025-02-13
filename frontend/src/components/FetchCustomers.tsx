import { useAuth } from "@clerk/clerk-react"; // Import Clerk hook
import AXIOS_API from "@/components/api";
import { useEffect, useState } from "react";

interface Customer {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
}

const FetchCustomerData = () => {
  const { getToken, isSignedIn } = useAuth(); // Get token from Clerk
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCustomer = async () => {
      if (!isSignedIn) {
        setError("User not logged in");
        setLoading(false);
        return;
      }

      try {
        const token = await getToken(); // ✅ Get Clerk JWT token
        console.log("Token being sent:", token); // Debugging

        const response = await AXIOS_API.get("/api/my-profile/", {
          headers: { Authorization: `Bearer ${token}` }, // ✅ Send token
        });

        setCustomer(response.data);
      } catch (error) {
        console.error(error);
        setError("Failed to fetch customer data");
      } finally {
        setLoading(false);
      }
    };

    fetchCustomer();
  }, [getToken, isSignedIn]); // ✅ Runs only when authentication state changes

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="bg-white p-4 shadow-md rounded-lg">
      <h2 className="text-xl font-semibold mb-2">Logged-in Customer</h2>
      {customer ? (
        <p>
          {customer.first_name} {customer.last_name} ({customer.email})
        </p>
      ) : (
        <p>No customer data available</p>
      )}
    </div>
  );
};

export default FetchCustomerData;
