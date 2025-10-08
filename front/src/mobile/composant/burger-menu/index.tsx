import type React from "react";
import "./burger.scss";
import { type RefObject, useEffect } from "react";

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

//How to use the component:
//  -> include mobile/composant/burger-menu
//  -> create the state and use the function for that tactile responsiveness
//    -> ``` const [open, setOpen] = useState(false);
//          const node = useRef<HTMLDivElement>(null);
//          useOnClickOutside(node, () => setOpen(false));
//        ```
//  -> open the burger-menu component with an `open` state (a boolean)
//    and the function to open/close the menu
//  -> put all the components you want inside of it
//  -> close the burger-menu component

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
