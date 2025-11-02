export { handleFormSubmit } from "./handleFormSubmit";

import "./style.scss";

interface FormSubmitButtonProps {
  value: string;
  className?: string;
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
}

export default function FormSubmitButton({
  value,
  className = "btn-validate",
  onClick,
}: FormSubmitButtonProps) {
  return (
    <button type="submit" className={"btn " + className} onClick={onClick}>
      {value}
    </button>
  );
}
