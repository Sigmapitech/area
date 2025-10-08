import type React from "react";
import "./burger.scss";
import { type RefObject, useEffect } from "react";

{
  /*
  How to use the component:
    -> include mobile/composant/burger-menu
    -> open the burger-menu component with an `open` state (a boolean)
      and the function to open/close the menu (follow example in the entrypoint.tsx file).
    -> put all the components you want inside of it
    -> close the burger-menu component
*/
}

interface BurgerProps {
  open: boolean;
  setOpen: (open: boolean) => void;
}

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
        type="button"
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
