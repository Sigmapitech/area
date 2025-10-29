import AREA from "../../../favicon.svg";
import "./style.scss";

import { useCallback, useEffect, useRef, useState } from "react";
import { Link, Outlet } from "react-router";
import { API_BASE_URL } from "@/api_url";
import { useAuth } from "@/auth";

export default function MainLayout() {
  const { token, logout } = useAuth();
  const [userInitial, setUserInitial] = useState("?");
  const [menuVisible, setMenuVisible] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

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

  const toggleMenu = () => {
    setMenuVisible((prev) => !prev);
  };

  const handleClickOutside = useCallback((event: MouseEvent) => {
    if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
      setMenuVisible(false);
    }
  }, []);

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [handleClickOutside]);

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
        {menuVisible && (
          <div
            role="menu"
            className="user-menu"
            onMouseDown={(e) => e.stopPropagation()}
          >
            <ul>
              <li>
                <Link to="/profile">
                  <span className="material-icons">person</span>
                  Profile
                </Link>
              </li>
              <li>
                <Link to="/settings">
                  <span className="material-icons">settings</span>
                  Settings
                </Link>
              </li>
              <li
                onClick={() => {
                  logout();
                }}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ") {
                    logout();
                  }
                }}
                // biome-ignore lint: element li is interactive.
                tabIndex={0}
              >
                <span className="material-icons">logout</span>
                Logout
              </li>
            </ul>
          </div>
        )}
      </header>

      <Outlet />
    </div>
  );
}
