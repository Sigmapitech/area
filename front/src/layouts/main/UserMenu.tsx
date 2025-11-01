import "./style.scss";

import {
  type Dispatch,
  type RefObject,
  type SetStateAction,
  useCallback,
  useEffect,
} from "react";

import { Link } from "react-router";
import { useAuth } from "@/auth";

import "./user-menu.scss";

interface UserMenuProps {
  menuRef: RefObject<HTMLDivElement | null>;
  menuVisible: boolean;
  setMenuVisible: Dispatch<SetStateAction<boolean>>;
}

export default function UserMenu({
  menuRef,
  menuVisible,
  setMenuVisible,
}: UserMenuProps) {
  const { logout } = useAuth();

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
    <>
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
    </>
  );
}
