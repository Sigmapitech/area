import AREA from "../../../favicon.svg";
import "./style.scss";

import { useEffect, useRef, useState } from "react";

import { Link, Outlet } from "react-router";
import { API_BASE_URL } from "@/api_url";
import { useAuth } from "@/auth";
import UserMenu from "./UserMenu";

export default function MainLayout() {
  const { token } = useAuth();
  const [userInitial, setUserInitial] = useState("?");
  const menuRef = useRef<HTMLDivElement>(null);

  const [menuVisible, setMenuVisible] = useState(false);

  const toggleMenu = () => {
    setMenuVisible((prev) => !prev);
  };

  useEffect(() => {
    if (!token) return;

    fetch(`${API_BASE_URL}/auth/me`, {
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

        <div className="user-icon-wrapper" ref={menuRef}>
          <button type="button" className="user-icon" onClick={toggleMenu}>
            <span className="user-icon-initial">{userInitial}</span>
          </button>
        </div>
        {
          <UserMenu
            menuRef={menuRef}
            menuVisible={menuVisible}
            setMenuVisible={setMenuVisible}
          />
        }
      </header>

      <Outlet />
    </div>
  );
}
