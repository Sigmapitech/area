import { StrictMode } from "react";

import "./style.scss";
import { Link } from "react-router";
import { useAuth } from "@/auth";

export default function HomePage() {
  const { token } = useAuth();

  if (!token) return;
  return (
    <StrictMode>
      <div className="home-page">
        <div className="buttons">
          <Link to="/workflow">Workflows</Link>
          <Link to="/services">Services</Link>
        </div>
      </div>
    </StrictMode>
  );
}
