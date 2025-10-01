import { Navigate, Outlet } from "react-router";
import { useAuth } from "./context";

export default function LoginRequired() {
  const { token } = useAuth();

  if (!token) return <Navigate to="/login" replace />;

  return <Outlet />;
}
