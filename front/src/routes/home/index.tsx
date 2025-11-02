import { StrictMode } from "react";

import "./style.scss";
import { Link } from "react-router";
import { useAuth } from "@/auth";

export default function HomePage() {
  const { logout } = useAuth();

  return (
    <StrictMode>
      <div className="home-page">
        <div className="buttons">
          <Link to="/workflow">Graph page</Link>
          <Link to="/services">Services</Link>
          <button type="button" onClick={logout}>
            Logout
          </button>
        </div>
      </div>
    </StrictMode>
  );
}
