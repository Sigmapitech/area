import React from "react";
import "./burger.scss";

interface BurgerProps {
  open: boolean;
  setOpen: (open: boolean) => void;
}

import { useEffect, type RefObject } from "react";

type EventType = TouchEvent;

export const useOnClickOutside = <T extends HTMLElement>(
  ref: RefObject<T | null>,
  handler: (event: EventType) => void
): void => {
  useEffect(() => {
    const listener = (event: EventType) => {
      const el = ref?.current;
      if (!el || el.contains(event.target as Node)) return;
      handler(event);
    };
    document.addEventListener("touchstart", listener);
    return () => {
      document.removeEventListener("touchstart", listener);
    };
  }, [ref, handler]);
};

const Burger: React.FC<BurgerProps & { children?: React.ReactNode }> = ({
  open,
  setOpen,
  children,
}) => {
  return (
    <div>
      <button
        className={`burger ${open ? "open" : ""}`}
        onClick={() => setOpen(!open)}
        aria-label="Toggle menu"
      >
        <div />
        <div />
        <div />
      </button>
      {open && (
        <div className="burger-content">
          <div className="burger-value">{children}</div>
        </div>
      )}
    </div>
  );
};

export default Burger;
