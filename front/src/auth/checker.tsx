import { useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router";
import { API_BASE_URL } from "@/api_url";
import { useAuth } from "./context";

export default function LoginRequired() {
  const { token } = useAuth();
  const [loading, setLoading] = useState(true);
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      setAuthorized(false);
      return;
    }

    const fetchMe = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error("Unauthorized");
        await res.json();
        setAuthorized(true);
      } catch {
        setAuthorized(false);
        setLoading(false);
      } finally {
        setLoading(false);
      }
    };

    fetchMe();
  }, [token]);

  if (!authorized && !loading) return <Navigate to="/login" replace />;

  return <Outlet />;
}
