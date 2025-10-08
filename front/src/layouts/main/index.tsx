import AREA from "../../../favicon.svg";
import "./style.scss";

import { useEffect, useState } from "react";
import { Link, Outlet } from "react-router";
import { API_BASE_URL } from "@/api_url";
import { useAuth } from "@/auth";

export default function MainLayout() {
  const { token } = useAuth();
  const [userInitial, setUserInitial] = useState("?");

  useEffect(() => {
    if (!token) return;

    fetch(`${API_BASE_URL}/api/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => response.json())
      .then((data) => {
        setUserInitial(data.name ? data.name.charAt(0).toUpperCase() : "X");
      })
      .catch((e) => {
        console.error(e);
      });
  }, [token]);

  return (
    <div className="main">
      <header className="main-bar">
        <Link to="/" className="home-link">
          <img src={AREA} height="24px" width="24px" alt="Area" />
          <span>Area</span>
        </Link>

        <div className="user-icon">
          <span className="user-icon-intial">{userInitial}</span>
        </div>
      </header>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
