import { useState } from "react";

import "./password-input.scss";

interface PasswordInputProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  name: string;
  placeholder?: string;
}

export default function PasswordInput({
  value,
  onChange,
  name,
  placeholder,
}: PasswordInputProps) {
  const [show, setShow] = useState(false);

  return (
    <div className="password-input">
      <input
        type={show ? "text" : "password"}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required
      />
      <button
        type="button"
        className="show-hide-btn"
        onClick={() => setShow((prev) => !prev)}
      >
        <span className="material-symbols-outlined">
          visibility{show ? "_off" : ""}
        </span>
      </button>
    </div>
  );
}
