import AREA from "../../../favicon.svg";
import home from "@material-design-icons/svg/round/home.svg";
import folder from "@material-design-icons/svg/round/folder.svg";
import density_medium from "@material-design-icons/svg/round/density_medium.svg";
import keyboard_arrow_down from "@material-design-icons/svg/round/keyboard_arrow_down.svg";
import "./style.scss";

import { API_BASE_URL } from "@/api_url";
import { useAuth } from "@/auth";

import { Link, useLocation } from "react-router";
import { useEffect, useState, type ReactNode } from "react";
import { Outlet } from "react-router";

export default function MainLayout() {
  const { token } = useAuth();
  const [userInitial, setUserInitial] = useState("X");

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => response.json())
      .then((data) => {
        setUserInitial(data.name ? data.name.charAt(0).toUpperCase() : "X");
      })
      .catch((e) => {
        console.error(e);
        setUserInitial("X");
      });
  }, [token]);

  const path = useLocation().pathname.split("/");
  const titleNodes: ReactNode[] = [
    <div key={`page`} className="text-wrapper">
      {path.length > 1 ? path[1] : "Home"}
    </div>,
  ];
  path.forEach((subname, i) => {
    // Add separator before all but first breadcrumb
    if (i > 0)
      titleNodes.push(
        <div key={`sep-${i}`} className="text-wrapper">
          /
        </div>
      );
    titleNodes.push(
      <div key={`b-${i}`} className="text-wrapper">
        {subname}
      </div>
    );
  });

  return (
    <div className="main">
      <div className="top-bar">
        <div className="top-left-corner">
          <Link to="/" className="vector-wrapper home-link">
            <img className="img" alt="Home" src={home} />
          </Link>
        </div>

        <div className="top-content">
          <div className="left">
            <div className="text-wrapper">-</div>

            <div className="app-title">
              <div className="vector-wrapper">
                <img className="img" alt="Area" src={AREA} />
              </div>

              <div className="text-wrapper">Area</div>
            </div>
          </div>

          <div className="center">
            <div className="vector-wrapper">
              <img className="img" alt="Folder" src={folder} />
            </div>
            {titleNodes}

            <div className="vector-wrapper">
              <img
                className="img"
                alt="Keyboard Arrow Down"
                src={keyboard_arrow_down}
              />
            </div>
          </div>

          <div className="right">
            <div className="user-icon">
              <div className="div">{userInitial}</div>
            </div>
          </div>
        </div>
      </div>

      <div className="center-content">
        <div className="left-bar">
          <div className="vector-wrapper">
            <img className="img" alt="Density Medium" src={density_medium} />
          </div>
        </div>

        <div className="main-content">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
